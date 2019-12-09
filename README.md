# Implementacija genetskog algoritma u programskom jeziku Python

**1. Predlog problema:**
Nalaženje što je moguće kraće rute izmedju dve tačke u dvodimenzionalnom prostoru. Ulazni parametri su koordinate polazne i krajnje tačke, kao i koordinate linije koja se nalazi izmedju tačaka i koju treba izbeći. Zadatak se sastoji u generisanju skupa linija (ruta) koje imaju pomenute tačke kao polazne i krajnje, a pritom linije ne seču liniju - ona predstavlja prepreku.

**2. Problem za primenu genetskog algoritma**
Osnovni problem je u činjenici da dvodimenzionalni prostor može da bude jako širok i da postoji veliki broj mogučih linija koje spajaju dve tačke i ispunjavaju uslov izbegavanja preprečne linije. Genetskim algoritmom se polazi od nasumično generisanog skupa linija (ruta) i napredovanjem generacija se očekuje dobijanje što je moguće efikasnijih putanja izmedju tačaka. Treba voditi računa da svaka putanja ispunjava uslov izbegavanja preprečne linije izmedju tačaka.

**3. Implementacija genetskog algoritma**
Za implementaciju algoritma se koriste samo osnovne biblioteke Python okruženja. S obzirom na složenost problema nije bilo neophodno koristiti open-source biblioteke. Predstavljanje DNA-a, kao i sve funkcije preklapanja i mutiranja su izgradjene od osnovnih biblioteka što dozvoljava veću fleksibilnost.

**3.1. Parametri genetskog algoritma**
Svi ulazni argumenti algoritma su parametrizovani.
1. *no_moves* - najveći broj dozvoljenih tačaka/skretanja linija (256)
2. *no_generations* - broj generacija (128)
3. *dna_size* - veličina DNA-a, duplo veća vrednost od *no_moves* (512)
4. *cross_rate* - stepen preklapanja (0.9)
5. *mutation_rate* - stepen mutacija (0.0001)
6. *pop_size* - prostor za generisanje nasumičnih vrednosti kod preklapanja (100)

Na slikama se može videti napredovanje algoritma. Polazna generacija je skup nasumično generisanih linija izmedju dve tačke. Svakom iteracijom dobija se manji skup linija koje zadovoljavaju uslove. Na kraju se očekuje što manji skup linija izmedju polazne i krajnje tačke sa što boljom ocenom kvaliteta - *fitness*.
 
![alt text][screenshot_algotithm_start]

[screenshot_algotithm_start]: metadata/algorithm-start.jpg

U konzolnom prozoru se nakon formiranja nove generacije prikazuje i *fitness* najbolje jedinke. Može se primetiti da je napredovanje najosetnije u početnim iteracijama algoritma, vremenom stagnira.

![alt text][screenshot_algotithm_end]

[screenshot_algotithm_end]: metadata/algorithm-end.jpg

## Implementacioni detalji
