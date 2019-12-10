## Implementacija genetskog algoritma u programskom jeziku Python

**1. Predlog problema:**
Nalaženje što je moguće kraće rute izmedju dve tačke u dvodimenzionalnom prostoru. Ulazni parametri su koordinate polazne i krajnje tačke, kao i koordinate linije koja se nalazi izmedju tačaka i koju treba izbeći. Zadatak se sastoji u generisanju skupa linija (ruta) koje imaju pomenute tačke kao polazne i krajnje, a pritom linije ne seču liniju - ona predstavlja prepreku.

**2. Problem za primenu genetskog algoritma**
Osnovni problem je u činjenici da dvodimenzionalni prostor može da bude jako širok i da postoji veliki broj mogučih linija koje spajaju dve tačke i ispunjavaju uslov izbegavanja preprečne linije. Genetskim algoritmom se polazi od nasumično generisanog skupa linija (ruta) i napredovanjem generacija se očekuje dobijanje što je moguće efikasnijih putanja izmedju tačaka. Treba voditi računa da svaka putanja ispunjava uslov izbegavanja preprečne linije izmedju tačaka.

**3. Implementacija genetskog algoritma**
Za implementaciju algoritma koriste se samo osnovne biblioteke Python okruženja. S obzirom na složenost problema nije neophodno koristiti open-source biblioteke. Predstavljanje DNA-a, kao i sve funkcije preklapanja i mutiranja su izgradjene od osnovnih biblioteka što dozvoljava veću fleksibilnost.

**3.1. Parametri genetskog algoritma**
Svi ulazni argumenti algoritma su parametrizovani.
1. *no_moves* - najveći broj dozvoljenih tačaka/skretanja svake linije (256)
3. *no_chromosomes* - broj hromozoma generacija (100)
4. *no_generations* - broj generacija (128)
5. *dna_size* - veličina DNA-a odnosno jednog hromozoma, duplo veća vrednost od *no_moves* (512)
6. *cross_rate* - stepen preklapanja (0.9)
7. *mutation_rate* - stepen mutacija (0.0001)
8. *dna_bound* - donja i gornja granica za nasumične vrednosti hromozoma na početku, kao i kasnije mutacije

Na slikama se može videti napredovanje algoritma. Polazna generacija je skup nasumično generisanih linija izmedju dve tačke. Svakom iteracijom dobija se manji skup linija koje zadovoljavaju uslove. Na kraju se očekuje što manji skup linija izmedju polazne i krajnje tačke sa što boljom ocenom kvaliteta - *fitness*.
 
![alt text][screenshot_algotithm_start]

[screenshot_algotithm_start]: metadata/algorithm-start.jpg

U konzolnom prozoru se nakon formiranja nove generacije prikazuje i *fitness* najbolje jedinke. Može se primetiti da je napredovanje najosetnije u početnim iteracijama algoritma, vremenom stagnira.

![alt text][screenshot_algotithm_end]

[screenshot_algotithm_end]: metadata/algorithm-end.jpg

## Implementacioni detalji

Klasa koja sadrži opisuje potrebna ponašanja nazvana je `GeneticAlgorithm`, njene metode su:
1. `__init__` za inicijalizaciju parametara
2. `dna_to_product` za konverziju DNA-a (generacije) u linije koje će biti isrtane
3. `get_fitness` za nalaženje fitness parametara svih jediniki generacije
4. `select` za izvlačenje parametara jedinke
5. `crossover` za preklpanja
6. `mutate` za mutacije
7. `evolve` za kombinovanje preklpanja i mutacija

### Inicijalizacija i metoda `__init__`
Na početku algoritma neophodno je oformiti nasumičnu generaciju kao polaznu tačku. U ovom koraku se parametrizuje genetski algoritam i sve vrednosti navedene na početku dokumenta su inicijalizovane vrednostima. Bitne vrednosti su na primer `dna_size` koja odredjuje dužinu hromozoma u svakoj generaciji, zatim `dna_bound` koja odredjuje granice početnih vrednosti i kasnijih mutacija svakog hromozoma.

```python
self.pop = numpy.random.randint(*dna_bound, size = (no_chromosomes, dna_size))
```

Ovo je polazna inicijalizacija i zadužena je za formiranje prve generacije. Generacija ima `no_chromosomes` elemenata od kojih svaki predstavlja niz od `no_moves` (x,y) tačaka u prostoru koje formiraju jednu liniju. U svakom trenutku se pristupa generaciji preko atributa `self.pop`.

### Kodiranje hromozoma
Hromozom se kodira sa `2 x no_moves` *pomeraja u prostoru* gde je svaki realan broj i realtivan u odnosu na prethodni pomeraj. Privh `no_moves` pomeraja je po x-osi, a isto toliko preostalih je po y-osi. Hromozom, prema tome, opisuje sve tačke koje čine jednu liniju u 2d prostoru, svaka od tačaka može i ne mora da bude skretanje linije. Neophodno je konvertovati pomeraje kojima je kodiran hromozom u stvarne tačke.

```python
self.pop[0] = [1, 1, 0, 1, 1, 0, 0, ...] [0:512]
...
self.pop[99] = [0, 1, 1, 1, 1, 0, ...] [0:512]
```

### Iscrtavanje linija i metoda `dna_to_product`
Ova metoda koristi se za konverziju svakog hromozoma u jednu liniju 2d-prostora. Neophodno je sve *pomeraje kojima je hromozom kodiran* sumirati i kao rezultat *sklopiti niz koordinata*. Ovo podrazumeva generisanje svih x/y tačaka a zatim i prosledjivanje istih metodi pomoćne klase `Line.plotting` koja će iscrtati sve tačke u prostoru. Povratne vrednosti su `lines_x` i `lines_y` matrice, svaki od redova(i) odgovara jednom hromozomu i sadrži niz svih pomeraja i-tog hromozoma prevedenih u koordinate.

### Mera dobrote i metoda `get_fitness`
Rezultat prethodne metode, odnosno nizovi koordinata `lines_x` i `lines_y` odgovaraju svakom hromozomu i ima ih ukupno `no_chromosomes`. Treba izračunati meru dobrote svakog od njih. Proces se svodi na nalaženje dobrote po principu udaljenosti od krajnje tačke. Uzimaju se u obzir krajnje x/y koordinate svakog hromozoma i meri njihova udaljenost od referentne tačke koju treba dostići.

Takodje, u početku postoje hromozomi koji su nasumično generisani i *ne odgovaraju uslovu tako što seku preprečnu liniju*. Neophodno je označiti koje linije nisu valjane. Svi hromozomi koji nisu valjani se označavaju jako malo mdobrotom od `1e-6`.

```python
def get_fitness(self, lines_x, lines_y, point_b, obstacle_line):
        distance_to_goal = numpy.sqrt((point_b[0] - lines_x[:, -1]) ** 2 + (point_b[1] - lines_y[:, -1]) ** 2)
        fitness = numpy.power(1 / (distance_to_goal + 1), 2)
```

Kao što se može videti, dobrota se računa na osnovu udaljenosti izmedju krajnje tačke linije i referentne odredišne tačke u prostoru po dobro poznatoj formuli. Ovakvom merom dobrote će hromozomi, odnosno linije koje predstavljaju, težiti odredišnoj tački kroz generacije.

### Selekcija hromozoma i metoda `select`