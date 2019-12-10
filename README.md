# Implementacija genetskog algoritma u programskom jeziku Python

**1. Predlog problema:**
Nalaženje što je moguće kraće rute izmedju dve tačke u dvodimenzionalnom prostoru. Ulazni parametri su koordinate polazne i krajnje tačke, kao i koordinate linije koja se nalazi izmedju tačaka i koju treba izbeći. Zadatak se sastoji u generisanju skupa linija (ruta) koje imaju pomenute tačke kao polazne i krajnje, a pritom linije ne seču liniju - ona predstavlja prepreku.

**2. Problem za primenu genetskog algoritma:**
Osnovni problem je u činjenici da dvodimenzionalni prostor može da bude jako širok i da postoji veliki broj mogučih linija koje spajaju dve tačke i ispunjavaju uslov izbegavanja preprečne linije. Genetskim algoritmom se polazi od nasumično generisanog skupa linija (ruta) i napredovanjem generacija se očekuje dobijanje što je moguće efikasnijih putanja izmedju tačaka. Treba voditi računa da svaka putanja ispunjava uslov izbegavanja preprečne linije izmedju tačaka.

**3. Implementacija genetskog algoritma:**
Za implementaciju algoritma koriste se samo osnovne biblioteke Python okruženja. S obzirom na složenost problema nije neophodno koristiti open-source biblioteke. Predstavljanje DNA-a, kao i sve funkcije preklapanja i mutiranja su izgradjene od osnovnih biblioteka što dozvoljava veću fleksibilnost.

**3.1. Parametri genetskog algoritma:**
Svi ulazni argumenti algoritma su parametrizovani.

1. **no_moves** - najveći broj dozvoljenih tačaka/skretanja svake linije (256)
2. **no_chromosomes** - broj hromozoma generacija (100)
3. **no_generations** - broj generacija (128)
4. **dna_size** - veličina DNA-a odnosno jednog hromozoma, duplo veća vrednost od *no_moves* (512)
5. **cross_rate** - stepen preklapanja (0.9)
6. **mutation_rate** - stepen mutacija (0.0001)
7. **dna_bound** - donja i gornja granica za nasumične vrednosti hromozoma na početku, kao i kasnije mutacije

Na slikama se može videti napredovanje algoritma. Polazna generacija je skup nasumično generisanih linija izmedju dve tačke. Svakom iteracijom dobija se manji skup linija koje zadovoljavaju uslove. Na kraju se očekuje što manji skup linija izmedju polazne i krajnje tačke sa što boljom ocenom kvaliteta - *fitness*.
 
![alt text][screenshot_algotithm_start]

[screenshot_algotithm_start]: metadata/algorithm-start.jpg

U konzolnom prozoru se nakon formiranja nove generacije prikazuje i **fitness** najbolje jedinke. Može se primetiti da je napredovanje najosetnije u početnim iteracijama algoritma, vremenom stagnira.

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
self.generation = numpy.random.randint(*dna_bound, size = (no_chromosomes, dna_size))
```

Ovo je polazna inicijalizacija i zadužena je za formiranje prve generacije. Generacija ima `no_chromosomes` elemenata od kojih svaki predstavlja niz od `no_moves` (x,y) tačaka u prostoru koje formiraju jednu liniju. U svakom trenutku se pristupa generaciji preko atributa `self.generation`.

### Kodiranje hromozoma

Hromozom se kodira sa `2 x no_moves` **pomeraja u prostoru** gde je svaki realan broj i realtivan u odnosu na prethodni pomeraj. Privh `no_moves` pomeraja je po x-osi, a isto toliko preostalih je po y-osi. Hromozom, prema tome, opisuje sve tačke koje čine jednu liniju u 2d-prostoru, svaka od tačaka može i ne mora da bude skretanje linije. Neophodno je konvertovati pomeraje kojima je kodiran hromozom u stvarne tačke.

```python
self.generation[0] = [1, 1, 0, 1, 1, 0, 0, ...] [0:512]
...
self.generation[99] = [0, 1, 1, 1, 1, 0, ...] [0:512]
```

### Iscrtavanje linija i metoda `dna_to_product`

Ova metoda koristi se za konverziju svakog hromozoma u jednu liniju 2d-prostora. Neophodno je sve **pomeraje kojima je hromozom kodiran** sumirati i kao rezultat **sklopiti niz koordinata**. Ovo podrazumeva generisanje svih x/y tačaka a zatim i prosledjivanje istih metodi pomoćne klase `Line.plotting` koja će iscrtati sve tačke u prostoru. Povratne vrednosti su `lines_x` i `lines_y` matrice, svaki od redova(i) odgovara jednom hromozomu i sadrži niz svih pomeraja i-tog hromozoma prevedenih u koordinate.

### Mera dobrote i metoda `get_fitness`

Rezultat prethodne metode, odnosno nizovi koordinata `lines_x` i `lines_y` odgovaraju svakom hromozomu i ima ih ukupno `no_chromosomes`. Treba izračunati meru dobrote svakog od njih. Proces se svodi na nalaženje dobrote po principu udaljenosti od krajnje tačke. Uzimaju se u obzir krajnje x/y koordinate svakog hromozoma i meri njihova udaljenost od referentne tačke koju treba dostići.

Takodje, u početku postoje hromozomi koji su nasumično generisani i **ne odgovaraju uslovu tako što seku preprečnu liniju**. Neophodno je označiti koje linije nisu valjane. Svi hromozomi koji nisu valjani se označavaju jako malom dobrotom od `1e-6`.

```python
def get_fitness(self, lines_x, lines_y, point_b, obstacle_line):
        distance_to_goal = numpy.sqrt((point_b[0] - lines_x[:, -1]) ** 2 + (point_b[1] - lines_y[:, -1]) ** 2)
        fitness = numpy.power(1 / (distance_to_goal + 1), 2)
```

Kao što se može videti, dobrota se računa na osnovu udaljenosti izmedju krajnje tačke linije i referentne odredišne tačke u prostoru po dobro poznatoj formuli. Ovakvom merom dobrote će hromozomi, odnosno linije koje predstavljaju, težiti odredišnoj tački kroz generacije.

### Selekcija hromozoma i metoda `select`

Pomoćna metoda koja se koristi u procesu evoluiranja. Potrebno je za svaki hromozom izabrati indeks roditelja. Verovatnoća izbora roditelja raste srazmerno njegovoj dobroti.

### Evoluiranje i metoda `evolve`

```python
def evolve(self, fitness):
    generation = self.select(fitness)
    generation_copy = generation.copy()
    for parent in generation:
        child = self.crossover(parent, generation_copy)
        child = self.mutate(child)
        parent[:] = child
    self.generation = generation
```

### Preklapanje jediniki i metoda `crossover`

```python
def crossover(self, parent, generation):
    if numpy.random.rand() < self.cross_rate:
        i_ = numpy.random.randint(0, self.no_chromosomes, size = 1) # select another individual from generation
        cross_points = numpy.random.randint(0, 2, self.dna_size).astype(numpy.bool) # choose crossover points
        parent[cross_points] = generation[i_, cross_points] # cross and produce one child
    return parent
```

Preklapanje, odnosno *crossover* sa izabranim roditeljem svodi se na nekoliko koraka. Prvo, treba izabrati nasumično hromozom sa kojim će se vršiti preklapanje. Zatim, nasumično generisati tačke preklapanja kao `boolean` vrednosti `True/False`. `True` vrednosti u nizu tačaka će značiti uzimanje vrednosti indeksa nasumično izabrane jedinke, ostale vrednosti u roditelju preostaju iste. Na kraju, do preklapanje ne mora da dodje, roditelj će biti nepromenjen u broju slučajeva srazmernom meri preklapanja `cross_rate`.

### Mutiranje jediniki i metoda `mutate`

```python
def mutate(self, child):
    for point in range(self.dna_size):
        if numpy.random.rand() < self.mutation_rate:
            child[point] = numpy.random.randint(*self.dna_bound)
    return child
```

Svaki novonastali hromozom može ali ne mora da mutira nakon neobaveznog koraka preklapanja. Nakon formiranja novog hromozoma po meri mutacije algoritma, neke od vrednosti u okviru deteta evoluiraju u granicama `dna_bound`. Na kraju, do mutiranja jedinke ne mora da dodje, jedinka može ostati nepromenjena u broju slučajeva srazmernom meri mutiranja `mutation_rate`.

### Primer evolucije hromozoma

Primer napredovanja hromozoma će biti prikazan u nastavku. Biće razmatran i-ti hromozom prve i poslednje generacije. U prilogu se može videti kodirani hromozom na početku algoritma, ovo je nasumično generisani niz pomeraja. Prva polovina vrednosti se odnosi na pomeraje po x-osi, ostatak na odgovarajuće pomeraje po y-osi.

```json
chromosome: ([0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1,
       1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1,
       0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
       0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0,
       0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1,
       1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0,
       1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
       1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
       1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1,
       1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1,
       1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1,
       1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1,
       0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1,
       1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
       1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1,
       0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1,
       1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1,
       0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
       1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
       0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1,
       0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0,
       1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0,
       1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1,
       0, 1, 1, 1, 1, 1])
```

Na kraju algoritma, i-ti hromozom iz poslednje generacije izgleda drugačije. Linija koja predstavlja evoluirani hromozom je validna s obzirom da ne seče preprečnu liniju, takodje je put izmedju polazne i krajnjne tačke znatno kraći. Vrednost dobrote hromozoma je očekivano veća u poredjenju sa istim na početku algoritma.

```json
chromosome: ([0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1,
       0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0,
       0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1,
       1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0,
       1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1,
       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1,
       0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1,
       0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0,
       1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0,
       1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1,
       0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0,
       0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1,
       0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0,
       1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
       0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1,
       0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
       1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0,
       0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0,
       1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1,
       0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0,
       0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1,
       1, 0, 1, 1, 0, 0])
```