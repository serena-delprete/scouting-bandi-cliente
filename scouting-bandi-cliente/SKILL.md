---
name: scouting-bandi-cliente
description: >-
  Qualifica un cliente di finanza agevolata e trova i bandi pubblici/privati che gli calzano, partendo dai suoi documenti (visura, statuto, atto costitutivo, bilancio/rendiconto, CV ente, progetti). Esegue due passi in sequenza: grounding del cliente (chi è, profilo strutturato, killer di mandato) e poi matching dei bandi (scouting + filtro eligibility + fit gradato). Usa questa skill ogni volta che si parla di onboarding/qualifica di un nuovo cliente bandi, di "scouting bandi", "quali bandi per [cliente]", "analizza questo cliente per la finanza agevolata", o quando viene fornita una cartella di documenti di un ente/impresa/ETS da valutare per i finanziamenti — anche se l'utente non nomina esplicitamente "Prompt 0" o "Prompt 1". NON usarla per il deep-dive di un singolo bando, la scrittura della proposta o il calcolo di fee/profittabilità (quelli sono prompt/skill successivi).
---

# Scouting bandi cliente (Prompt 0 + Prompt 1)

Questa skill copre il primo tratto della catena di consulenza in finanza agevolata: **da un cliente ai bandi candidabili**. Lavora in due passi che corrispondono a due prompt collaudati, qui inclusi come riferimenti:

1. **Grounding (Prompt 0)** — `references/prompt_0_grounding.md` (v1.5)
2. **Matching bandi (Prompt 1)** — `references/prompt_1_matching.md` (v1.1)

Fermati qui: deep dive su un singolo bando, redazione proposta e valutazione fee/profittabilità sono fuori scope (prompt/skill successivi). Se l'utente chiede quelle cose, dillo e rimanda.

## Quando si attiva

Tipico: l'utente ha una **cartella di documenti** di un ente/impresa/ETS (o li carica) e vuole sapere chi è il cliente e quali bandi gli calzano. Oppure chiede esplicitamente lo scouting per un cliente già profilato.

## Passo 0 — Ingestione documenti (sempre, prima di tutto)

Il grounding vale quanto i dati che riesci a leggere. I documenti reali dei clienti sono spesso **PDF scansionati, file firmati `.p7m`, docx, xlsx, immagini** — non testo pulito. NON limitarti a `pdftotext`: molti documenti chiave (statuto, atto costitutivo, verbali organi, rendiconti) sono scansioni che danno zero testo senza OCR, e saltarli falsa il grounding.

Usa lo script bundled che gestisce tutti i formati (testo PDF, OCR tesseract per le scansioni, docx, xlsx, p7m firmati, immagini):

```bash
bash scripts/extract_docs.sh "<cartella_documenti_cliente>" > /tmp/grezzo_<cliente>.txt
```

Lo script è robusto su cartelle grandi (50+ file): fa OCR solo delle **prime 6 pagine** per PDF scansionato (`MAX_PAGES`), ha un **timeout per file** (`OCR_TIMEOUT=60s`) e **salta i moduli amministrativi ripetitivi** (mod01-05, ritenuta, tracciabilità, conflitto interessi, ecc.) che non portano profilo (`SKIP_ADMIN=1`). Override via variabili d'ambiente se serve di più. **Su cartelle molto grandi punta a una sottocartella rilevante** (es. solo i documenti istituzionali/finanziari) invece della radice: è più veloce e l'OCR sull'intero archivio rischia di rallentare. Senza questi accorgimenti su archivi grossi lo script può impallarsi — perciò non rimuoverli.

Poi leggi `/tmp/grezzo_<cliente>.txt`. Se un documento risulta `non_leggibile_tecnico` anche dopo l'OCR, segnalalo (P7 del Prompt 0) e procedi con il resto, marcando i campi mancanti.

In alternativa, se i documenti sono su Google Drive collegato, il connettore `read_file_content` estrae testo anche da PDF/immagini (OCR server-side) e i Google Doc sono testo puro — usalo quando la cartella vive sul Drive del cliente.

## Passo 1 — Grounding (Prompt 0)

Leggi `references/prompt_0_grounding.md` e applicalo al testo estratto. Produce un output a **3 livelli** (Cruscotto + Dettaglio operativo con Scheda Cliente campi 1-29 + Allegato strutturato) e un verdetto su 5 stati (DENTRO / DENTRO con condizioni / FUORI / IN ATTESA / NON DECIDIBILE).

**Salva la Scheda Cliente come file** `scheda_cliente_<nome>.md` nella cartella del cliente: è un asset che vive nel tempo e alimenta sia il Passo 2 sia i prompt successivi. Indica sempre la **completezza %** e lo stato di ogni campo (confermato / da_verificare / da_chiedere / non_rilevante / da_formalizzare).

Rispetta i principi del Prompt 0: dati grezzi prima dei giudizi; distingui dato dichiarato da inferenza; non inventare numeri (campo assente → `da_chiedere`); applica le regole R1-R11 e i killer mandato K1-K5; per ETS/enti pubblici marca `non_rilevante` ciò che non si applica (es. dimensione UE, GBER) invece di forzarlo.

## Passo 2 — Matching bandi (Prompt 1)

Leggi `references/prompt_1_matching.md` e applicalo ai **Livelli 2 e 3 della Scheda** (non al Cruscotto). Produce: Cruscotto bandi (fit alto/medio + gap sanabili in tempo), dettaglio per bando, allegato. Workflow in 3 fasi: scouting → filtro requisiti soggettivi (tassonomia KS/GS/FG) → fit gradato.

**Il calendario predittivo (bandi ricorrenti che apriranno nei prossimi mesi) NON va sepolto nel Livello 3**: rendilo una sezione esplicita e in evidenza, perché è azionabile e interessa direttamente il cliente. Includi ≥3 bandi ricorrenti pertinenti al profilo.

## Passo 3 — Sintesi cliente (mostrabile)

I tre output del Passo 1-2 (Scheda 3 livelli, Dossier mandato, lista bandi tecnica) sono **interni**: contengono verdetto, killer, R-codes, inquadramento di portafoglio — roba che per il Prompt 0 è *confidenziale e non si mostra mai al cliente*. Servono a te e all'intreccio con le skill successive, e vanno bene dettagliati.

Ma il cliente ha bisogno di un documento **diverso**: corto, leggibile, senza gergo interno. Produci sempre anche `sintesi_cliente_<nome>.md`:

- **Chi siete** (3-4 righe neutre: cosa fa l'ente, dimensione, punti di forza). Niente verdetto DENTRO/FUORI, niente killer.
- **Bandi consigliati** in linguaggio piano: nome, a cosa serve, perché vi calza, cosa serve preparare. NIENTE codici KS/GS/FG, R-xx, fit 🟢/🟡 — traducili ("forte coerenza", "richiede un partner UE", "da localizzare in Lombardia").
- **Calendario prossime aperture**: i bandi ricorrenti con stima mese di apertura, così il cliente sa cosa aspettare.
- **Prossimi passi**: 3-5 azioni concrete (verificare ROC, rinnovare organi, raccogliere documento X), in tono collaborativo.

Tienila a **1-2 pagine**. È il documento che il consulente può girare al cliente senza editarlo.

Output finale della skill (tre file salvati):
1. `scheda_cliente_<nome>.md` — dettagliata, interna, per l'intreccio con le skill successive.
2. `lista_bandi_<nome>.md` — matching tecnico (fit, gap, tassonomia), interna.
3. `sintesi_cliente_<nome>.md` — **mostrabile al cliente**, neutra, in linguaggio piano, con calendario e prossimi passi.

## Lezioni operative (non ripeterle a vuoto, ma rispettale)

Sono errori reali emersi sul campo. Tienili presenti perché cambiano il risultato:

- **La geografia delle fondazioni NON è un killer.** Un bando di una fondazione fuori regione (es. Cariplo in Lombardia per un cliente del Lazio) NON va escluso: se il vincolo è sulla *localizzazione del progetto* (S4.c, immediato) e non sulla sede legale, è soddisfacibile localizzando le attività. Tratta come killer geografico solo i vincoli di **sede** (S4.a), non quelli di realizzazione-progetto.
- **Distingui finanziamenti incassati da patrocini/endorsement.** Nel track record (campo 15) conta ciò che ha prodotto fondi reali. Non stare a spaccare il capello tra "patrocinio" e "grant" se il patrocinio ha portato un grant; se non ha portato nulla, non mapparlo affatto.
- **Cofinanziamento del cliente = vincolo forte se la cassa è bassa.** Per micro-ETS/clienti con poca liquidità (R10 basso), privilegia bandi a **fondo perduto con anticipo significativo**; segnala come fit basso i bandi a solo saldo finale o con cofinanziamento alto. Leggilo dai rendiconti reali, non a sentimento.
- **Non sovra-analizzare.** L'obiettivo è la decisione utile ("questo cliente è dentro, questi bandi gli calzano, questi gap vanno chiusi"), non il dibattito tassonomico. Se ti accorgi di stare producendo distinzioni che non cambiano una scelta, taglia.

## Iterazione

Se arrivano nuovi documenti dopo un primo grounding, NON ricominciare da zero: versiona la Scheda (v1.0 → v1.X), aggiorna i campi cambiati, riverifica i campi dinamici (compliance, DURC, organi, plafond) e i bandi nuovi/scaduti dalla versione precedente (vedi sez. 9 dei due prompt).
