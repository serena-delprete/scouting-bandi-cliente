#!/usr/bin/env python3
"""
pmi_sizing.py — Calcolo dimensione PMI UE (Raccomandazione 2003/361/CE)

Usato dalla Chain Prompt Finanza Agevolata (P0a Extractor → questo script → P0b Evaluator).
Il P0a estrae i numeri grezzi dai documenti del cliente; questo script li classifica.

Soglie UE:
  Micro:   addetti < 10   AND (fatturato ≤ 2M  OR totale bilancio ≤ 2M)
  Piccola: addetti < 50   AND (fatturato ≤ 10M OR totale bilancio ≤ 10M)
  Media:   addetti < 250  AND (fatturato ≤ 50M OR totale bilancio ≤ 43M)
  Grande:  tutto il resto

Regola: l'impresa può scegliere il criterio finanziario più favorevole
(fatturato O totale bilancio), non è obbligatorio soddisfare entrambi.

Consolidamento (Art. 3):
  - Impresa autonoma: nessun consolidamento
  - Impresa associata (partecipazione 25%-50%): si aggiunge la quota proporzionale
  - Impresa collegata (partecipazione >50%): si aggiunge il 100%

Autrice: Serena Del Prete (con assistenza Claude)
Versione: 1.0 — 2026-10-05
Licenza: MIT (coerente con repo GitHub scouting-bandi-cliente)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DimensioneUE(Enum):
    """Classificazione dimensionale UE."""
    MICRO = "micro"
    PICCOLA = "piccola"
    MEDIA = "media"
    GRANDE = "grande"


class TipoRelazione(Enum):
    """Tipo di relazione proprietaria con altra impresa."""
    ASSOCIATA = "associata"      # 25%-50% partecipazione
    COLLEGATA = "collegata"       # >50% partecipazione


@dataclass
class ImpresaCorrelata:
    """Dati di un'impresa associata o collegata."""
    denominazione: str
    tipo_relazione: TipoRelazione
    quota_partecipazione: float  # 0.0-1.0 (es. 0.30 = 30%)
    addetti: Optional[float] = None
    fatturato_eur: Optional[float] = None
    totale_bilancio_eur: Optional[float] = None
    fonte: str = ""
    data_fonte: str = ""


@dataclass
class DatiImpresa:
    """Dati grezzi dell'impresa target estratti dal P0a."""
    denominazione: str
    addetti: Optional[float] = None          # ULA (unità lavorative anno)
    fatturato_eur: Optional[float] = None    # ultimo esercizio chiuso
    totale_bilancio_eur: Optional[float] = None
    fonte_addetti: str = ""
    fonte_fatturato: str = ""
    fonte_bilancio: str = ""
    data_fonte: str = ""                     # data del bilancio di riferimento
    correlate: list[ImpresaCorrelata] = field(default_factory=list)


@dataclass
class RisultatoClassificazione:
    """Output strutturato della classificazione."""
    dimensione: DimensioneUE
    addetti_consolidati: Optional[float]
    fatturato_consolidato: Optional[float]
    totale_bilancio_consolidato: Optional[float]
    autonoma: bool
    dettaglio_consolidamento: list[str]  # righe di spiegazione
    avvertenze: list[str]               # warning (dati mancanti, inferenze)
    calcolabile: bool                   # False se dati insufficienti


# ---------------------------------------------------------------------------
# Soglie (Raccomandazione 2003/361/CE, Allegato, Art. 2)
# ---------------------------------------------------------------------------
SOGLIE = {
    DimensioneUE.MICRO:   {"addetti": 10,  "fatturato": 2_000_000,  "bilancio": 2_000_000},
    DimensioneUE.PICCOLA: {"addetti": 50,  "fatturato": 10_000_000, "bilancio": 10_000_000},
    DimensioneUE.MEDIA:   {"addetti": 250, "fatturato": 50_000_000, "bilancio": 43_000_000},
}


def _consolida(impresa: DatiImpresa) -> tuple[Optional[float], Optional[float], Optional[float], bool, list[str]]:
    """
    Calcola i valori consolidati secondo Art. 3 della Raccomandazione.

    Returns:
        (addetti, fatturato, bilancio, è_autonoma, dettaglio_righe)
    """
    addetti = impresa.addetti
    fatturato = impresa.fatturato_eur
    bilancio = impresa.totale_bilancio_eur
    dettaglio: list[str] = []

    if not impresa.correlate:
        return addetti, fatturato, bilancio, True, ["Impresa autonoma — nessun consolidamento."]

    dettaglio.append(f"Impresa target: addetti={_fmt(addetti)}, fatturato={_fmt_eur(fatturato)}, bilancio={_fmt_eur(bilancio)}")

    for corr in impresa.correlate:
        if corr.tipo_relazione == TipoRelazione.COLLEGATA:
            # >50%: si aggiunge il 100% dei valori
            moltiplicatore = 1.0
            label = f"COLLEGATA ({corr.quota_partecipazione:.0%}→100%)"
        else:
            # 25%-50%: si aggiunge la quota proporzionale
            moltiplicatore = corr.quota_partecipazione
            label = f"ASSOCIATA ({corr.quota_partecipazione:.0%})"

        riga = f"  + {corr.denominazione} [{label}]:"
        contributi = []

        if corr.addetti is not None and addetti is not None:
            contributo_addetti = corr.addetti * moltiplicatore
            addetti += contributo_addetti
            contributi.append(f"addetti +{contributo_addetti:.1f}")

        if corr.fatturato_eur is not None and fatturato is not None:
            contributo_fatt = corr.fatturato_eur * moltiplicatore
            fatturato += contributo_fatt
            contributi.append(f"fatturato +{_fmt_eur(contributo_fatt)}")

        if corr.totale_bilancio_eur is not None and bilancio is not None:
            contributo_bil = corr.totale_bilancio_eur * moltiplicatore
            bilancio += contributo_bil
            contributi.append(f"bilancio +{_fmt_eur(contributo_bil)}")

        if contributi:
            riga += " " + ", ".join(contributi)
        else:
            riga += " dati non disponibili (non consolidabile)"

        dettaglio.append(riga)

    dettaglio.append(f"Consolidato: addetti={_fmt(addetti)}, fatturato={_fmt_eur(fatturato)}, bilancio={_fmt_eur(bilancio)}")
    return addetti, fatturato, bilancio, False, dettaglio


def _classifica(addetti: Optional[float], fatturato: Optional[float], bilancio: Optional[float]) -> Optional[DimensioneUE]:
    """
    Applica le soglie UE. L'impresa può scegliere il criterio finanziario più favorevole.

    Returns:
        DimensioneUE o None se dati insufficienti per classificare.
    """
    if addetti is None:
        return None

    # Test dal più piccolo al più grande: la prima soglia che regge vince
    for dim in [DimensioneUE.MICRO, DimensioneUE.PICCOLA, DimensioneUE.MEDIA]:
        soglia = SOGLIE[dim]
        if addetti >= soglia["addetti"]:
            continue

        # Per il criterio finanziario basta soddisfarne UNO (il più favorevole)
        if fatturato is not None and fatturato <= soglia["fatturato"]:
            return dim
        if bilancio is not None and bilancio <= soglia["bilancio"]:
            return dim

        # Se entrambi i criteri finanziari sono disponibili e ENTRAMBI sforano → next
        if fatturato is not None and bilancio is not None:
            continue

        # Se un solo criterio finanziario è disponibile e sfora → next
        if fatturato is not None or bilancio is not None:
            continue

        # Nessun dato finanziario: classifica solo su addetti (con avvertenza)
        return dim

    return DimensioneUE.GRANDE


def classifica_impresa(impresa: DatiImpresa) -> RisultatoClassificazione:
    """
    Entry point principale. Prende i dati grezzi e restituisce la classificazione.

    Usabile direttamente dal P0b Evaluator o da qualsiasi script che abbia
    i dati estratti dal P0a.
    """
    avvertenze: list[str] = []

    # Validazione input
    if impresa.addetti is None:
        avvertenze.append("CRITICO: addetti (ULA) non disponibili — classificazione impossibile senza questo dato.")

    if impresa.fatturato_eur is None and impresa.totale_bilancio_eur is None:
        avvertenze.append("WARNING: né fatturato né totale bilancio disponibili — classificazione basata solo su addetti (se disponibili).")

    # Verifica soglie partecipazione
    for corr in impresa.correlate:
        if corr.tipo_relazione == TipoRelazione.ASSOCIATA:
            if not (0.25 <= corr.quota_partecipazione <= 0.50):
                avvertenze.append(
                    f"WARNING: {corr.denominazione} marcata ASSOCIATA ma quota {corr.quota_partecipazione:.0%} "
                    f"fuori range 25%-50%. Se <25% → autonoma (ignorare). Se >50% → collegata."
                )
        elif corr.tipo_relazione == TipoRelazione.COLLEGATA:
            if corr.quota_partecipazione <= 0.50:
                avvertenze.append(
                    f"WARNING: {corr.denominazione} marcata COLLEGATA ma quota {corr.quota_partecipazione:.0%} "
                    f"≤50%. Verificare: se 25%-50% → associata."
                )

    # Consolidamento
    addetti_c, fatturato_c, bilancio_c, autonoma, dettaglio = _consolida(impresa)

    # Classificazione
    dimensione = _classifica(addetti_c, fatturato_c, bilancio_c)
    calcolabile = dimensione is not None

    if not calcolabile:
        avvertenze.append("Classificazione non calcolabile — servono almeno gli addetti (ULA).")
        dimensione = DimensioneUE.GRANDE  # fallback conservativo

    return RisultatoClassificazione(
        dimensione=dimensione,
        addetti_consolidati=addetti_c,
        fatturato_consolidato=fatturato_c,
        totale_bilancio_consolidato=bilancio_c,
        autonoma=autonoma,
        dettaglio_consolidamento=dettaglio,
        avvertenze=avvertenze,
        calcolabile=calcolabile,
    )


# ---------------------------------------------------------------------------
# Output formattato (per integrazione con P0b o uso CLI)
# ---------------------------------------------------------------------------

def _fmt(val: Optional[float]) -> str:
    if val is None:
        return "n.d."
    if val == int(val):
        return str(int(val))
    return f"{val:.1f}"


def _fmt_eur(val: Optional[float]) -> str:
    if val is None:
        return "n.d."
    if val >= 1_000_000:
        return f"€{val/1_000_000:.2f}M"
    if val >= 1_000:
        return f"€{val/1_000:.1f}K"
    return f"€{val:.0f}"


def formato_report(risultato: RisultatoClassificazione) -> str:
    """Produce un blocco di testo Markdown inseribile nel P0b output."""
    lines = []
    lines.append(f"**Dimensione UE: {risultato.dimensione.value.upper()}**")

    if not risultato.calcolabile:
        lines.append("⚠️ *Classificazione non calcolabile — fallback conservativo a GRANDE.*")

    lines.append("")
    lines.append(f"| Parametro | Valore consolidato |")
    lines.append(f"|---|---|")
    lines.append(f"| Addetti (ULA) | {_fmt(risultato.addetti_consolidati)} |")
    lines.append(f"| Fatturato | {_fmt_eur(risultato.fatturato_consolidato)} |")
    lines.append(f"| Totale bilancio | {_fmt_eur(risultato.totale_bilancio_consolidato)} |")
    lines.append(f"| Autonoma | {'Sì' if risultato.autonoma else 'No (consolidamento applicato)'} |")

    if risultato.dettaglio_consolidamento:
        lines.append("")
        lines.append("Dettaglio consolidamento:")
        for riga in risultato.dettaglio_consolidamento:
            lines.append(f"  {riga}")

    if risultato.avvertenze:
        lines.append("")
        lines.append("Avvertenze:")
        for a in risultato.avvertenze:
            lines.append(f"  ⚠️ {a}")

    return "\n".join(lines)


def to_json_dict(risultato: RisultatoClassificazione) -> dict:
    """Serializza il risultato in dict per il JSON intermedio P0a→P0b."""
    return {
        "dimensione_ue": risultato.dimensione.value,
        "calcolabile": risultato.calcolabile,
        "addetti_consolidati": risultato.addetti_consolidati,
        "fatturato_consolidato": risultato.fatturato_consolidato,
        "totale_bilancio_consolidato": risultato.totale_bilancio_consolidato,
        "autonoma": risultato.autonoma,
        "dettaglio_consolidamento": risultato.dettaglio_consolidamento,
        "avvertenze": risultato.avvertenze,
    }


# ---------------------------------------------------------------------------
# CLI: uso standalone per test rapidi
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys

    # Esempio 1: PMI manifatturiera autonoma
    esempio_autonoma = DatiImpresa(
        denominazione="Alfa Manifatturiera SRL",
        addetti=45,
        fatturato_eur=8_500_000,
        totale_bilancio_eur=6_200_000,
        fonte_addetti="Bilancio 2024",
        fonte_fatturato="Bilancio 2024",
        fonte_bilancio="Bilancio 2024",
        data_fonte="2025-04-30",
    )

    # Esempio 2: PMI con controllata (collegata >50%)
    esempio_consolidata = DatiImpresa(
        denominazione="Beta Tech SRL",
        addetti=30,
        fatturato_eur=4_000_000,
        totale_bilancio_eur=3_500_000,
        fonte_addetti="Bilancio 2024",
        data_fonte="2025-04-30",
        correlate=[
            ImpresaCorrelata(
                denominazione="Gamma Digital SRL",
                tipo_relazione=TipoRelazione.COLLEGATA,
                quota_partecipazione=0.80,
                addetti=15,
                fatturato_eur=2_000_000,
                totale_bilancio_eur=1_800_000,
                fonte="Visura camerale",
                data_fonte="2025-03-15",
            ),
            ImpresaCorrelata(
                denominazione="Delta Innovation SRL",
                tipo_relazione=TipoRelazione.ASSOCIATA,
                quota_partecipazione=0.35,
                addetti=200,
                fatturato_eur=40_000_000,
                totale_bilancio_eur=35_000_000,
                fonte="Bilancio consolidato",
                data_fonte="2025-04-30",
            ),
        ],
    )

    # Esempio 3: ETS micro senza dati finanziari completi
    esempio_ets = DatiImpresa(
        denominazione="B-HOP Magazine APS",
        addetti=0.5,
        fatturato_eur=None,  # ETS non ha fatturato, ha entrate
        totale_bilancio_eur=11_555,
        fonte_bilancio="Rendiconto 2024",
        data_fonte="2025-03-31",
    )

    print("=" * 60)
    for nome, dati in [
        ("Autonoma (piccola attesa)", esempio_autonoma),
        ("Consolidata (verifica soglie)", esempio_consolidata),
        ("ETS micro", esempio_ets),
    ]:
        print(f"\n--- {nome}: {dati.denominazione} ---\n")
        r = classifica_impresa(dati)
        print(formato_report(r))
        print(f"\nJSON:\n{json.dumps(to_json_dict(r), indent=2, ensure_ascii=False)}")
        print()
    print("=" * 60)
