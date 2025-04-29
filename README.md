# financial-news-insights
This project collects, cleans and analyses stock prices and related news in an automated way, allowing you to identify correlations between market trends and news.


---

## 📘 Projekt: Pénzügyi és Híradatok Integrált Elemzése

### 🎯 Célkitűzés

- **Webes adatgyűjtés:** Gyűjts adatokat pénzügyi weboldalakról és híroldalakról.
- **API-k használata:** Használj nyilvános API-kat pénzügyi és híradatok lekérésére.
- **Adattisztítás és -feldolgozás:** Tisztítsd meg és strukturáld az adatokat elemzéshez.
- **Adatvizualizáció:** Készíts grafikonokat és diagramokat az adatok szemléltetésére.

---

## 🗂️ Feladatok Listája

### 1. 📥 Adatok Gyűjtése

1. **Pénzügyi adatok lekérése API-n keresztül:**
   - Használj nyilvános API-kat (pl. Yahoo Finance) részvényárfolyamok lekérésére.

2. **Híradatok lekérése API-n keresztül:**
   - Használj hírszolgáltató API-kat (pl. NewsAPI) pénzügyi hírek lekérésére.

3. **Webes adatgyűjtés pénzügyi híroldalakról:**
   - Használj webes adatgyűjtési technikákat (pl. BeautifulSoup) pénzügyi híroldalak cikkeinek lekérésére.

### 2. 🧹 Adattisztítás és -feldolgozás

4. **Adatok átalakítása Pandas DataFrame-be:**
   - Alakítsd át az API-kból és webes adatgyűjtésből származó adatokat Pandas DataFrame-ekbe.

5. **Hiányzó értékek kezelése:**
   - Azonosítsd és kezeld a hiányzó értékeket az adatokban.

6. **Dátumformátumok egységesítése:**
   - Egységesítsd az időbélyegeket az adatokban.

7. **Szöveges adatok előfeldolgozása:**
   - Tisztítsd meg a szöveges adatokat (pl. hírcímek, összefoglalók) az elemzéshez.

8. **Adatok egyesítése:**
   - Egyesítsd a különböző forrásokból származó adatokat egy közös adatstruktúrába.

### 3. 📊 Adatvizualizáció

9. **Idősoros grafikonok készítése:**
   - Készíts grafikonokat a részvényárfolyamok időbeli alakulásáról.

10. **Hírek megjelenésének időbeli eloszlása:**
    - Vizualizáld a hírek megjelenésének időbeli eloszlását.

11. **Hírek és árfolyamváltozások összefüggései:**
    - Készíts grafikonokat, amelyek bemutatják a hírek és az árfolyamváltozások közötti összefüggéseket.

12. **Szöveges adatok vizualizációja:**
    - Készíts szófelhőket vagy egyéb vizualizációkat a hírek szöveges tartalmának elemzéséhez.

### 4. 🧠 Elemzés és Következtetések

13. **Statisztikai elemzések készítése:**
    - Számítsd ki az átlagos, medián és szórás értékeket a részvényárfolyamokra vonatkozóan.

14. **Korrelációs elemzés:**
    - Vizsgáld meg a hírek és az árfolyamváltozások közötti korrelációt.

15. **Idősoros elemzés:**
    - Elemezd az árfolyamok időbeli trendjeit és szezonális mintázatait.

16. **Sentiment elemzés (opcionális):**
    - Végezz érzelemelemzést a hírek szöveges tartalmán, és vizsgáld meg annak hatását az árfolyamokra.

---

Az alábbiakban bemutatok egy részletes listát a pénzügyi és üzleti elemzési riportok típusairól, amelyek hasznosak lehetnek a projekted során. Ezek a riportok segítenek megérteni a vállalat pénzügyi helyzetét, teljesítményét és jövőbeli kilátásait.

---

## 📊 Fő pénzügyi riportok

1. **Mérleg (Balance Sheet)**
   -A vállalat eszközeit, forrásait és saját tőkéjét mutatja egy adott időpontban
   -Segít megérteni a vállalat likviditását és tőkeszerkezetét
   -Kulcsfontosságú mutatók: eszközök, kötelezettségek, saját tőke

2. **Eredménykimutatás (Income Statement)**
   -A bevételek, költségek és nyereség vagy veszteség alakulását mutatja egy adott időszakban
   -Segít értékelni a vállalat jövedelmezőségét és működési hatékonyságát
   -Kulcsfontosságú mutatók: bruttó nyereség, üzemeltetési költségek, nettó nyereség

3. **Cash Flow kimutatás (Cash Flow Statement)**
   -A pénzeszközök beáramlását és kiáramlását mutatja három fő tevékenységi kör szerint: működés, befektetés, finanszírozás
   -Segít megérteni a vállalat pénzügyi egészségét és likviditását
   -Kulcsfontosságú mutatók: működési cash flow, befektetési cash flow, finanszírozási cash flow

4. **Saját tőke változásainak kimutatása (Statement of Shareholders' Equity)**
   -A vállalat saját tőkéjének változásait mutatja egy adott időszakban
   -Segít megérteni a részvényesi érdekeltségek alakulását és a tőkeemeléseket vagy -csökkentéseket
   -Kulcsfontosságú mutatók: tőkeemelés, osztalékfizetés, részvénykibocsátás

---

## 📈 Elemző és kiegészítő riportok

5. **Kimutatás a működési eredményről (Operating Profit Report)**
    A vállalat fő tevékenységéből származó nyereséget mutatj.
    Segít megérteni a vállalat alaptevékenységeinek jövedelmezőségé.
    Kulcsfontosságú mutatók: működési nyereség, működési költsége.

6. **Bruttó árrés elemzés (Gross Margin Analysis)**
    A bruttó nyereség és a bevételek arányát mutatj.
    Segít megérteni a termelési költségek hatékonyságát és az árképzési stratégiá.
    Kulcsfontosságú mutatók: bruttó árrés, eladási ár, előállítási költsé.

7. **Részvényesi hozam elemzés (Shareholder Return Analysis)**
    A részvényesek által elért hozamokat mutatj.
    Segít értékelni a vállalat részvényesi értékteremtésé.
    Kulcsfontosságú mutatók: osztalék, részvényárfolyam növekedé.

8. **Likviditási mutatók elemzése (Liquidity Ratios Analysis)**
    A vállalat rövid távú pénzügyi helyzetét mutatj.
    Segít megérteni a vállalat képességét a rövid távú kötelezettségek teljesítésér.
    Kulcsfontosságú mutatók: gyorsráta, likviditási mutat.

9. **Adósság és tőkeáttétel elemzés (Debt and Leverage Analysis)**
    A vállalat adósságállományát és tőkeáttételi mutatóit vizsgálj.
    Segít megérteni a vállalat pénzügyi kockázatait és tőke struktúrájá.
    Kulcsfontosságú mutatók: adósság/ saját tőke arány, kamatfedezeti mutat.

10. **Részvényárfolyam elemzés (Stock Price Analysis)**
    - A vállalat részvényárfolyamának alakulását mutatja.
    - Segít megérteni a piac által a vállalatra adott értékelést.
    - Kulcsfontosságú mutatók: részvényárfolyam, piaci kapitalizáció.

11. **Pénzügyi előrejelzés (Financial Forecasting)**
    - A jövőbeli pénzügyi teljesítmény előrejelzését tartalmazza.
    - Segít a stratégiai döntéshozatalban és a tervezésben.
    - Kulcsfontosságú mutatók: bevételi előrejelzés, költségvetés, nyereség előrejelzés.

12. **Kockázatelemzés (Risk Analysis)**
    - A vállalat pénzügyi és működési kockázatait vizsgálja.
    - Segít azonosítani és kezelni a potenciális veszély 