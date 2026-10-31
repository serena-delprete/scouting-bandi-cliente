# Chain Prompt Finanza Agevolata

**Sette prompt in sequenza che portano i documenti grezzi di un cliente fino a una proposta progettuale completa — e che si fermano prima, quando il bando non è vincibile.**

---

## Il punto: filtrare, non accelerare

Su un caso reale, partendo da 7 bandi trovati:

```
7 bandi analizzati
   ↓  P2 — 6 check di fattibilità
4 fattibili          (3 bloccati: cofinanziamento, partenariato, scala)
   ↓  P3 — redazione sui criteri del finanziatore
2 proposte redatte
   ↓  P4 — pricing e valore atteso
1 approvata          GO con condizioni, fee flat
```

I 3 bandi bloccati sono il vero prodotto. Erano tutti bandi EU che sulla carta sembravano adatti e che avrebbero assorbito ore di lavoro prima di rivelarsi incompatibili con un ente da €11k di bilancio. La chain li ferma al check di fattibilità, prima della scrittura.

---

## La catena — 7 anelli

| # | Prompt | Input | Output |
|---|---|---|---|
| **0a** | Extractor | documenti cliente (visura, statuto, bilancio, progetti) | JSON strutturato, campi 1-29 |
| **0b** | Evaluator | JSON da 0a | Scheda Cliente + dossier mandato + killer di mandato |
| **1** | Matching | Scheda Cliente | scouting bandi + filtro eleggibilità + fit gradato |
| **2** | Fattibilità | bandi candidati | timeline + 6 check per bando (cofinanziamento, documenti, tempo, partenariato, rischi, competitività) |
| **3** | Redazione | scheda fattibilità di 1 bando + regolamento | proposta completa: testi, budget, Gantt, mappatura criteri |
| **3.5** | Compilazione piattaforma | draft P3 | trasferimento sulla piattaforma del bando, verifica pre-invio |
| **4** | Pricing | scheda cliente + fattibilità + draft | GO/NO-GO, effort, 3 modelli di fee, cash flow, valore atteso |

Script di supporto: `pmi_sizing.py` — classificazione dimensionale UE (Racc. 2003/361/CE).

Ogni anello produce tre livelli: un cruscotto da leggere in trenta secondi, il dettaglio completo, e un allegato strutturato che alimenta l'anello successivo. Il consulente legge il cruscotto, decide, avanza.

---

## Guardalo funzionare

`examples/` contiene gli output reali su **B-HOP Magazine** — APS, testata registrata, bilancio annuo €11.555. Dal filtro dei 7 bandi fino al pricing.

`case_studies/bhop_magazine_it.html` racconta lo stesso caso in forma leggibile ([versione inglese](case_studies/bhop_magazine_en.html)).

---

## Limiti dichiarati

- **Testata su 2 clienti.** Il secondo (una Srl dell'economia circolare, usata per verificare che la chain reggesse anche fuori dal non profit) non è pubblicato qui: sono dati di un'azienda terza.
- **Una proposta redatta, nessuna inviata.** La finestra della Tavola Valdese apre a gennaio 2027.
- **Nessun bando vinto.** La chain non è ancora stata validata da un esito.
- **L'anello 3.5 non è mai stato provato su una piattaforma vera.** È l'unico scritto e non testato.
- **Le ore di effort nel case study sono stime**, non misurazioni cronometrate.
- **B-HOP è l'associazione dell'autrice.** Questo dà accesso a documenti e bilanci reali; va saputo.
- `scouting-bandi-cliente/` impacchetta come skill i **primi due anelli** (grounding + matching). Gli altri cinque girano in conversazione.

---

## Principi

- **Dati grezzi prima dei giudizi**: raccogli, poi valuta.
- **Mai forzare il match**: se il bisogno non è coerente col profilo, segnala, non inventare.
- **Dati incompleti sono una feature**: con un profilo al 59% la chain scrive SOSPESO, non "probabilmente ok".
- **Due piani separati**: Scheda Cliente neutra e mostrabile al cliente, dossier mandato confidenziale.

---

## Struttura

```
prompt_0a … prompt_4      i sette anelli
pmi_sizing.py             classificazione PMI UE
examples/                 output reali B-HOP
case_studies/             il caso in forma leggibile (IT + EN)
scouting-bandi-cliente/   skill: primi due anelli
archive/                  materiale storico, non necessario alla lettura
```

Licenza MIT. Costruita da [Serena Del Prete](https://www.linkedin.com/in/serenadelprete/) — ottobre 2026.
