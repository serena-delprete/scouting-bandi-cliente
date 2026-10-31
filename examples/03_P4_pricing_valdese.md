# TEST P4 v1.0 — B-HOP Magazine APS × Tavola Valdese OPM 2027

> **Modalità A** (post-P3). Dati da: test_P2 (7/10/2026), test_P3 (9/10/2026), sito b-hop.it.
> Parametri consulente: **default prudenziali** (€40/h, 60h/mese, €300 min, rischio medio, portfolio value no).
> Data test: 15 ottobre 2026. Autore: Claude (sub-agente Chain Prompt & Skill A).

---

## LIVELLO 1 — CRUSCOTTO DECISIONALE

```
═══ CRUSCOTTO VALUTAZIONE MANDATO ═══
Cliente: B-HOP Magazine APS                Data valutazione: 15/10/2026
Bando: Tavola Valdese OPM 2027             Tipo: contributo fondazione (OPM)
Importo bando: non definito (no tetto)     Importo accessibile al cliente: €10.500 (richiesta)

EFFORT STIMATO: 22 ore (≈3 giorni lavorativi)
FEE PROPOSTA: €880 (flat fee, fattore complessità 1.0)
MARGINE: €0 (tariffa effettiva = €40/h = target)
PROBABILITÀ SUCCESSO: 30% (base 35% − aggiustamenti)
VALORE ATTESO (se success fee): −€220 ⚠️
VALORE ATTESO (se flat fee): +€880 ✅
BREAK-EVEN FEE FLAT: €880
TEMPO DI RITORNO: 2-3 mesi (flat) / 12-18 mesi (success)

VERDETTO: GO CON CONDIZIONI
MOTIVAZIONE: Mandato economicamente marginale (fee €880 su micro ETS). 
GO solo se: (1) flat fee pagata all'invio, (2) il mandato produce il primo 
case study completo della chain P0→P4 (portfolio value), (3) Patrizia 
fornisce i dati mancanti entro dicembre senza eccessivo follow-up.

⏭️ Dettaglio calcoli: Livello 2. Fattori non-economici: Livello 3.
```

---

## LIVELLO 2 — DETTAGLIO CALCOLI

### EFFORT BREAKDOWN

Fonti: draft P3 (9 sezioni, 5 gap informativi ridotti a 0.5, piattaforma JUNO, budget 8 voci, Gantt 12 mesi).

| Fase | Ore stimate | Costo opportunità (€) | Note |
|---|---|---|---|
| Analisi bando + griglia | 2 | 80 | Già fatto in P2. Residuo: verifica LG 2027 quando pubblicate |
| Raccolta dati cliente | 4 | 160 | 0.5 gap residui (audience). Patrizia è reattiva ma va seguita |
| Redazione proposta | 8 | 320 | 9 sezioni, criteri qualitativi (no punteggi → stima pesi). Draft P3 copre ~70%, serve rifinitura con dati reali |
| Revisioni | 3 | 120 | 1-2 cicli con Patrizia. Stima conservativa |
| Compilazione piattaforma JUNO | 3 | 120 | Prima volta su JUNO per il consulente. Include: registrazione, navigazione campi, upload allegati, check finale |
| Amministrazione | 2 | 80 | Contratto, comunicazioni, fatturazione |
| **TOTALE** | **22** | **€880** | Buffer +20% già incluso nelle stime per fase |

### PRICING

**Modello scelto: flat fee** (raccomandato per micro ETS con importo bando <€15k).

Calcolo:
- Ore stimate: 22
- Tariffa oraria target: €40/h
- Fattore complessità: 1.0 (bando standard, criteri qualitativi ma struttura nota, piattaforma nuova ma gestibile)
- **Fee flat = 22 × €40 × 1.0 = €880**

Modelli alternativi (per confronto):

| Modello | Fee | Condizione | Tariffa effettiva/h |
|---|---|---|---|
| Flat fee | €880 | Pagamento a invio candidatura | €40/h |
| Success fee 10% | €1.050 | Solo se vinto | €47.7/h se vinto, €0 se perso |
| Success fee 15% | €1.575 | Solo se vinto | €71.6/h se vinto, €0 se perso |
| Misto 50/50 | €440 anticipo + 5% success (€525 se vinto) | Anticipo + variabile | €20/h garantiti + €23.9/h se vinto |

**Raccomandazione**: flat fee €880. Su un importo richiesto di €10.500, una fee di €880 = 8.4% del finanziamento — entro il range calibrato per micro ETS (8-15%). Il success fee puro ha valore atteso negativo (vedi sotto), quindi non è sostenibile.

### CASH FLOW

```
TIMELINE:
Mese 0 (gen 2027):  Firma mandato. Nessun anticipo (flat fee a invio).
                     Inizio lavoro: raccolta dati + rifinitura draft.
Mese 1 (gen-feb):   Redazione + revisioni + JUNO. Uscita: 22 ore = €880 costo opp.
Mese 1-2 (feb):     Invio candidatura su JUNO (scadenza attesa feb-mar 2027).
                     → Incasso fee flat: €880
Mese 5-8 (giu-set): Esito bando (tipicamente 4-6 mesi dopo scadenza Valdese).
                     Se success fee: incasso solo ora.
Mese 8-14:          Erogazione finanziamento (se vinto). 
                     Se success fee legata a erogazione: incasso solo ora.

ESPOSIZIONE MASSIMA: €880 (tutte le ore investite prima dell'incasso)
ESPOSIZIONE CON FLAT FEE: €0 dopo l'invio (fee incassata)
TEMPO DI RITORNO: 1-2 mesi (flat fee) / 8-14 mesi (success fee)
```

### PROBABILITÀ E VALORE ATTESO

**Probabilità base**: 35% (contributo fondazione, range 20-50%, posizionato al centro)

**Aggiustamenti**:
- Forza cliente su criteri: **−5 pp**. Criteri qualitativi Valdese senza punteggi. B-HOP forte su mission/coerenza (C1✅ C3✅ C4✅) ma debole su track record bandi (C2⚠️: 1 solo bando presentato, mai vinto Valdese prima) e cofinanziamento (C5⚠️: solo valorizzazione volontariato, no cash cofin)
- Competitività stimata (C6 P2): **−3 pp**. Valdese OPM è competitivo (nazionale, molte APS candidate). B-HOP non ha storico con Valdese
- Track record ente erogatore: **+3 pp**. Tavola Valdese ha trasparenza elevata, pubblica esiti, valutazione prevedibile

**Probabilità aggiustata: 30%**

```
VALORE ATTESO PER MODELLO:

Flat fee:      100% × €880 − €880 costo ore = €0 (neutro — copertura costi)
Success 10%:   30% × €1.050 − €880 = €315 − €880 = −€565 ❌
Success 15%:   30% × €1.575 − €880 = €472 − €880 = −€408 ❌
Misto 50/50:   €440 + 30% × €525 − €880 = €440 + €157 − €880 = −€283 ❌
```

**Conclusione**: solo la flat fee ha valore atteso non negativo. Il success fee puro è insostenibile a probabilità 30%.

### BREAK-EVEN

```
Ore stimate: 22
Costo ore (costo opportunità @€40/h): €880

Fee minima flat: €880 (= costo ore)
Fee minima success (se prob. 30%): €2.933 (= €880 / 0.30) — IRREALISTICA su €10.500 erogato (28%)
Fee minima mista (50% flat + success @30%): anticipo €440 + success fee minima €1.467 — IRREALISTICA
```

Solo il modello flat regge.

---

## LIVELLO 3 — ALLEGATO STRUTTURATO

### 5.3.1 Fattori non-economici

| Fattore | Valore | Impatto su decisione |
|---|---|---|
| Portfolio / case study | **ALTO** | Primo mandato end-to-end della chain P0→P4. Produce il case study per GitHub repo + portfolio Product Ops. Valore stimato: se genera anche solo 1 cliente futuro @€2.000 fee → ROI positivo |
| Referenza cliente | **MEDIO** | B-HOP ha visibilità (Il Fatto, ANSA, premio Campidoglio) ma non nel circuito bandi. Referenza utile per settore ETS/cultura, non per imprese |
| Learning | **ALTO** | Prima esperienza su piattaforma JUNO. Primo bando Valdese OPM. Primo bando con criteri qualitativi senza punteggi. Tre "primi" = apprendimento alto |
| Relazione ricorrente | **SÌ** | B-HOP ha pipeline P2 con 7 bandi. Se Valdese va bene → Cariplo, CERV, altri OPM. Cliente potenzialmente ricorrente |
| Rischio reputazionale | **BASSO** | Patrizia è collaborativa (già lavorato insieme su Comune Roma). Nessun rischio se il bando non viene vinto — Valdese è competitivo, è atteso |
| Costo opportunità reale | **BASSO** | 22 ore su 60 disponibili/mese = 37% della capacità mensile. Non preclude altri mandati. Periodo gen-feb tipicamente bassa stagione bandi |

### 5.3.2 Scenari alternativi

| Scenario | Fee | Prob. | Valore atteso | Verdetto |
|---|---|---|---|---|
| **Base (flat fee)** | €880 | 100% (pagamento a invio) | €0 (copertura costi) | GO CON CONDIZIONI |
| Ottimistico (prob. +10pp, success) | €1.050 success | 40% | −€460 | NO-GO |
| Pessimistico (prob. −10pp, success) | €1.050 success | 20% | −€670 | NO-GO |
| Flat fee con portfolio value (+€500 stimato) | €880 + €500 futuro | 100% incasso + 50% portfolio | €880 + €250 − €880 = +€250 | GO |
| Flat fee maggiorata (complessità 1.2) | €1.056 | 100% | +€176 | GO |

**Scenario raccomandato**: flat fee €880 con portfolio value implicito. Se il case study genera anche 1 referral futuro, il mandato è in attivo.

### 5.3.3 Proposta commerciale suggerita (bozza)

```
Oggetto: Proposta di consulenza — Bando Tavola Valdese OPM 2027

Gentile Patrizia,

a seguito dell'analisi del bando Otto per Mille della Chiesa Evangelica Valdese 
(edizione 2027), propongo il seguente servizio di consulenza per la candidatura 
di B-HOP Magazine APS.

SERVIZIO: redazione completa della proposta progettuale per la piattaforma JUNO
- Analisi criteri di valutazione e posizionamento strategico
- Stesura narrativa progettuale (obiettivi, contesto, attività, risultati, sostenibilità)
- Budget dettagliato e cronoprogramma 12 mesi
- Compilazione e upload su piattaforma JUNO
- 1-2 cicli di revisione prima dell'invio

COMPENSO: €880 (fee fissa, IVA esente — regime APS)
TEMPISTICA: 3-4 settimane dalla conferma
PAGAMENTO: a completamento dell'invio su JUNO

Il servizio comprende:
- Analisi del regolamento e dei criteri di valutazione
- Stesura testi, budget e cronoprogramma
- Compilazione piattaforma JUNO con upload allegati
- Fino a 2 cicli di revisione

Il servizio NON comprende:
- Raccolta documenti interni B-HOP (bilanci, statuto, CV — già in archivio)
- Gestione post-invio (comunicazioni con Tavola Valdese, integrazioni)
- Rendicontazione progetto (se finanziato — oggetto di accordo separato)

Resto a disposizione per un confronto.
Serena
```

### 5.3.4 Note di retroazione

**Verso P3**:
- L'effort P4 (22 ore) è coerente con il range "contributo fondazione" (15-30 ore). Nessuna correzione necessaria.
- Il draft P3 copre ~70% della proposta finale. Il 30% residuo è: dati reali B-HOP (audience, contatti scuole) + adattamento a LG 2027 + fine-tuning JUNO.

**Verso P0b**:
- Bilancio B-HOP €11.555 → la fee flat €880 = 7.6% del bilancio annuo. Sostenibile ma non trascurabile per una micro APS. Se Patrizia manifesta difficoltà a pagare, valutare: (a) misto con anticipo ridotto €300 + success 5%, oppure (b) scambio servizi (es. articolo su B-HOP per portfolio consulente).

**Verso P2**:
- Probabilità P4 (30%) è coerente col verdetto P2 (FATTIBILE con ⚠️ su C2 track record e C5 cofinanziamento). Nessuna contraddizione.
- La competitività C6 P2 era qualitativa ("medio-alta competitività"). P4 la traduce in −3 pp sulla probabilità base — aggiustamento conservativo.

---

## NOTA METODOLOGICA

Questo test usa i **parametri consulente default** (€40/h, 60h/mese, €300 min). I risultati cambiano significativamente se Serena fornisce i parametri reali — in particolare:

- Se tariffa target > €40/h → la fee flat sale e il mandato potrebbe diventare NO-GO per il cliente (€880 è già alto per una micro APS)
- Se tariffa target < €40/h → il mandato diventa più sostenibile
- Se portfolio value = sì → il verdetto passa da GO CON CONDIZIONI a GO pieno
- Se soglia fee minima > €880 → il mandato è automaticamente NO-GO

**Azione richiesta**: Serena deve configurare i parametri reali prima di usare P4 in produzione.
