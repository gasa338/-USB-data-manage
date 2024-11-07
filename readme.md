# USB File Copier

Ovaj projekat je desktop aplikacija koja omogućava automatsko kopiranje video fajlova sa USB uređaja na računar. Aplikacija koristi konfiguracioni fajl sa uređaja za generisanje validnog imena foldera u koji se kopiraju podaci. Tokom kopiranja, aplikacija beleži sve relevantne informacije u log fajl (`usb_copy.log`), uključujući vreme, status kopiranja, greške i druge podatke.

## Kako funkcioniše aplikacija

1.  **Kopiranje fajlova sa USB uređaja**  
   Aplikacija omogućava korisnicima da prebacuju video fajlove sa USB memorije na računar. Fajlovi imaju specifične nazive sastavljene od brojeva.
 
   Svaki uređaj sadrži konfiguracioni fajl, koji se čita prilikom povezivanja uređaja. Na osnovu podataka u konfiguracionom fajlu, aplikacija generiše validno ime za folder na računaru u koji će biti kopirani podaci.

2. **Čitanje konfiguracije**  
   Aplikacija učitava konfiguracioni fajl i na osnovu tih podataka kreira validno ime za folder na računaru.

3. **Kopiranje fajlova**  
   Aplikacija započinje kopiranje fajlova sa USB uređaja u odgovarajući folder na računaru, dok istovremeno beleži sve podatke u log fajl.

4. **Log fajl (`usb_copy.log`)**  
   Ovaj log fajl sadrži informacije o procesu kopiranja, uključujući vreme početka i završetka kopiranja, status kopiranja (uspešno, neuspešno), greške (ako postoje), kao i druge relevantne podatke.

## Nadogradnje

1. **Notifikacije o početku i završetku kopiranja**  
   Aplikacija sada šalje notifikacije korisnicima putem e-maila pri početku i završetku procesa kopiranja. Ovo omogućava korisnicima da budu obavešteni bez potrebe da stalno prate aplikaciju.

2. **Poboljšana funkcionalnost log fajla**  
   Log fajl ne samo da se čuva lokalno na računaru, već sada postoji opcija da se pošalje putem e-maila. Ova funkcionalnost omogućava dalju analizu procesa kopiranja ili dijagnostiku u slučaju grešaka.
