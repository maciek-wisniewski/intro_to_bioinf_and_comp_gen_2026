# Zadanie 3: Analiza danych Hi-C i integracja z danymi 1D

_Wstęp do Bioinformatyki i Genomiki Obliczeniowej, 2026_

**Maksymalna liczba punktów: 20 pkt**

Celem zadania jest przeprowadzenie analizy danych Hi-C oraz integracja wyników z dodatkowymi danymi genomowymi.

---

## 1. Wizualizacja danych Hi-C

Pobierz jeden z dostępnych zbiorów danych Hi-C (np. człowiek: GM12878, HUVEC, IMR90; mysz; muszka owocowa).  

Źródło danych (przykładowe):  
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63525

Następnie:
- Wczytaj dane przy użyciu wybranej biblioteki (np. `cooler`, `hic2cool`, `FAN-C`, `hic-straw`)
- Zwizualizuj wybrany region genomowy (heatmapa kontaktów)
- Krótko opisz obserwowane struktury

---

## 2. Detekcja TAD-ów

Zidentyfikuj TAD-y (Topologically Associating Domains) jedną ze znanych metod, np.
- directionality index
- insulation score
- lub inna metoda własna lub dostępna w bibliotece.

Następnie:
- Porównaj otrzymane TAD-y z danymi referencyjnymi (pobranymi z bazy danych).
- Oceń zgodność (wizualnie i ilościowo)

---

## 3. Analiza motywów CTCF

Zidentyfikuj wystąpienia motywów CTCF. Wykorzystaj dowolne narzędzie (np. skanowanie motywów PWM)

Następnie:
- Sprawdź, czy granice TAD-ów są wzbogacone w motywy CTCF (tzn. czy motywów CTCF jest tam średnio więcej niż w losowym miejscu w genomie)
- (*opcjonalnie): Przeanalizuj orientację motywów względem granic TAD-ów.

---

## 4. Integracja z danymi 1D (ATAC-seq / ChIP-seq)

Pobierz dane 1D **dla tego samego typu komórki**:
- ChIP-seq dla CTCF ATAC-seq

Następnie:
- Zwizualizuj sygnał wzdłuż wybranego regionu razem z mapą Hi-C
- Sprawdź, czy granice TAD-ów:
  - pokrywają się z peak-ami sygnału
- Wykonaj prostą analizę wzbogacenia (np. średni sygnał wokół granic TAD-ów vs regiony losowe)

---

## 5. (Opcjonalnie) Detekcja pętli chromatynowych

Spróbuj zidentyfikować pętle chromosomowe:
- używając dostępnych narzędzi (np. `FAN-C`, HiCCUPS)
- ..albo implementując własną metodę

Następnie:
- Porównaj wyniki z danymi referencyjnymi (jeśli dostępne)
- Oceń zgodność jakościowo i ilościowo

---

## Wymagania

- Kod (notebook lub skrypty)
- Krótki raport w formie prezentacji (opis metod, wyniki, wizualizacje, wnioski)
- Czytelne figury ilustrujące kluczowe etapy analizy

---