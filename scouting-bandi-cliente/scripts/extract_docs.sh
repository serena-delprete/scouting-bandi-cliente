#!/usr/bin/env bash
# Estrae testo da una cartella di documenti cliente (finanza agevolata).
# Gestisce: PDF testo (pdftotext), PDF scansionati (OCR tesseract), docx, xlsx, p7m firmati, immagini.
# Robusto su cartelle grandi: cap pagine OCR, timeout per file, skip moduli amministrativi non informativi.
#
# Uso:   extract_docs.sh "<cartella_cliente>" > grezzo.txt
# Tuning (variabili d'ambiente opzionali):
#   MAX_PAGES=6      # pagine OCR max per PDF scansionato (evita impallamento su PDF lunghi)
#   OCR_TIMEOUT=60   # secondi max per OCR di un singolo file
#   SKIP_ADMIN=1     # 1 = salta i moduli amministrativi ripetitivi (default); 0 = processa tutto
# Per cartelle molto grandi, conviene puntare a una sottocartella rilevante invece che alla radice.
set -uo pipefail
DIR="${1:?Uso: extract_docs.sh <cartella_cliente>}"
MAX_PAGES="${MAX_PAGES:-6}"
OCR_TIMEOUT="${OCR_TIMEOUT:-60}"
SKIP_ADMIN="${SKIP_ADMIN:-1}"
OCR_LANG="$(tesseract --list-langs 2>/dev/null | grep -qx ita && echo ita || echo eng)"
# moduli amministrativi senza info di profilo: si saltano per default
SKIP_RE='mod0[1-5]|ritenut|tracciabilit|conflitto.?interess|codificazione.?creditore|regime.?iva|domanda.?partecipazione|smime|\.p7s$'
emit(){ echo; echo "########## FILE: $1 ##########"; }
ocr_pdf(){ # $1=pdf ; OCR solo prime MAX_PAGES pagine, con timeout
  local tmp; tmp=$(mktemp -d)
  timeout "$OCR_TIMEOUT" pdftoppm -f 1 -l "$MAX_PAGES" -r 200 -png "$1" "$tmp/p" 2>/dev/null
  local tot; tot=$(pdfinfo "$1" 2>/dev/null | awk '/^Pages:/{print $2}'); tot=${tot:-?}
  for img in "$tmp"/p*.png; do [ -e "$img" ] || continue; timeout "$OCR_TIMEOUT" tesseract "$img" stdout -l "$OCR_LANG" 2>/dev/null; done
  [ "$tot" != "?" ] && [ "$tot" -gt "$MAX_PAGES" ] 2>/dev/null && echo "[...OCR limitato alle prime $MAX_PAGES di $tot pagine...]"
  rm -rf "$tmp"
}
skipped=0
find "$DIR" -type f \( -iname '*.pdf' -o -iname '*.docx' -o -iname '*.xlsx' -o -iname '*.xlsm' -o -iname '*.p7m' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) | sort | while read -r f; do
  if [ "$SKIP_ADMIN" = "1" ] && echo "$f" | grep -Eiq "$SKIP_RE"; then skipped=$((skipped+1)); continue; fi
  ext="${f##*.}"; ext="${ext,,}"
  case "$ext" in
    pdf)
      txt=$(pdftotext -layout "$f" - 2>/dev/null)
      if [ "$(printf '%s' "$txt" | tr -d '[:space:]' | wc -c)" -lt 40 ]; then emit "$f (PDF scansionato -> OCR)"; ocr_pdf "$f"; else emit "$f (PDF testo)"; printf '%s\n' "$txt"; fi ;;
    docx) emit "$f (docx)"; python3 -c "import docx,sys; print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" "$f" 2>/dev/null ;;
    xlsx|xlsm) emit "$f (xlsx)"; python3 -c "import openpyxl,sys; wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True);[print('|'.join(str(c) for c in r if c is not None)) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) if any(r)]" "$f" 2>/dev/null ;;
    p7m) base="${f%.p7m}"; out="/tmp/$(basename "$base")"; openssl smime -verify -noverify -inform DER -in "$f" -out "$out" 2>/dev/null && { emit "$f (p7m -> estratto)"; if [[ "$out" == *.pdf ]]; then t=$(pdftotext -layout "$out" - 2>/dev/null); if [ "$(printf '%s' "$t" | tr -d '[:space:]' | wc -c)" -lt 40 ]; then ocr_pdf "$out"; else printf '%s\n' "$t"; fi; fi; } ;;
    jpg|jpeg|png) emit "$f (immagine -> OCR)"; timeout "$OCR_TIMEOUT" tesseract "$f" stdout -l "$OCR_LANG" 2>/dev/null ;;
  esac
done
echo; echo "########## NOTA: $skipped file amministrativi saltati (SKIP_ADMIN=$SKIP_ADMIN). MAX_PAGES=$MAX_PAGES, OCR_TIMEOUT=${OCR_TIMEOUT}s ##########"
