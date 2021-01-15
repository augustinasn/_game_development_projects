from flask import render_template, url_for, redirect, request
from flask_app import app
from firebase import firebase

import os
import random

firebase = firebase.FirebaseApplication('https://mystery-box-ktu.firebaseio.com/',
                                        None)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/analitika")
def analytics():
    return render_template('analysis.html', title='Analitika')

@app.route("/analitika_sunkus_load")
def analytics_hard_load():
    redirect_to = url_for('analytics_hard')
    return render_template('loading.html', title='Kraunasi...', redirect=redirect_to)

@app.route("/analitika_sunkus")
def analytics_hard():

    questions_list = [("Jūs esate užrištomis akimis. Ant stalo yra 10 monetų, 5 iš jų herbų į viršų, kitos 5 – skaičiumi. Monetas galite vartyti kiek norite kartų, bet negalite atskirti kuria jos puse. Monetas turite atskirti į dvi krūveles po 5 (atsitiktinai), jūsų tikslas jas vartyti tol, kol abi pusės sutaps, t.y. turės po tiek pat herbų ir skaičių. Kiek mažiausiai vertimų reikia, kad abi pusės sutaptų garantuotai kiekvieną kartą. Sutapimo pavyzdys: <br> <img src='static/monetos.jpg'/>",
                       "Atskirkite bet kaip, tarkime gausite: HHHHS ir SSSSH, tada apverskite visas monetas vienoje iš krūvelių, tarkime pirmoje. Gautas rezultatas: SSSSH ir SSSSH. Atsakymas 5 vertimai."),
                      ("Du traukiniai važiuoja vienas į kitą, abiejų traukinių grečiai po 40 km/h. Atstumas tarp traukinių yra 80 km. Traukiniams pajudėjus, paukštis pradeda skristi nuo pirmojo traukinio iki antrojo, pasiekęs antrąjį traukinį, paukštis skrendą atgal iki pirmojo ir taip toliau, paukščio greitis 100 km/h. Kiek bus nuskridęs paukštis, kai traukiniai susidurs?",
                       "Bendras greitis v_b = v_t + v_t = 40 + 40 = 80 km/h. t = s/v = 100/80 = 1,25 h. s_p = v_p * t = 100 * 1,25 = 125 km."),
                      ("Maiše yra 20 mėlynų ir 13 raudonų kamuolių, traukiame du kamuolius, jei kamuoliai yra vienodų spalvų – juos išimame ir įdedame vieną mėlyną, jei kamuoliai skirtingų spalvų – juos išimame ir vietoj jų įdedame vieną raudoną. Kokios spalvos bus paskutinis kamuolys? Argumentuoti.",
                       "Po kiekvieno traukimo raudonų kamuolių skaičius visada yra nelyginis, todėl visada bandant ištraukti paskutinį raudoną kamuolį, bus įdėtas raudonas. Todėl paskutinis likęs kamuolys – raudonas."),
                      ("Turime dvi virves, jos yra skirtingos, abi netolygaus ilgio ir storio, vienintelė turima bendra savybė, kad virvė dega valandą. Kaip suskaičiuoti 45 minutes.",
                       "Padegame pirmą virvę iš abiejų galų, o antrąją iš vieno galo. Pirmoji virvė dega valandą, bet kadangi ji padegta iš abiejų galų – sudegs per 30 minučių. Kai sudegs pirmoji iškarto uždegame antrosios kitą galą, kadangi antrajai degti liko 30 minučių, o dega iš abiejų galų, tai pilnai sudegs per 15."),
                      ("Keturi žmonės skuba į susitikimą naktį, kad jie suspėtų, jiems reikia pereiti per tiltą per 17 minučių. Per tiltą, galima eiti nedaugiau kaip dviese ir reikalingas žibintuvėlis, žibintuvėlį turi tik vieną. A tiltą pereina per 1 minutę, B – 2min, C – 5min, D – 10min, kokia seka jiems reikia eiti, kad spėtų laiku.",
                       "A ir B eina į priekį (2min), A grįžta atgal (2+1=3 min), C ir D eina į priekį (3+10=13 min), B grįžta atgal (13+2=15min), A ir B eina į priekį (15+2=17min).")]

    random_choice =  random.choice(questions_list)
    q = f"Klausimas: {random_choice[0]}"
    a = f"Atsakymas: {random_choice[1]}"


    return render_template('analysis_hard.html', title='Analitika sunkus', q=q, a=a)

@app.route("/analitika_lengvas_load")
def analytics_easy_load():
    redirect_to = url_for('analytics_easy')
    return render_template('loading.html', title='Kraunasi...', redirect=redirect_to)

@app.route("/analitika_lengvas")
def analytics_easy():

    questions_list = [("Yra trys stiklainiai: “Obuoliai”, “Apelsinai”, “Obuoliai ir apelsinai”. VISI stiklainiai turi neteisingas etiketes. Galima traukti vieną vaisių ir tikrinti, kiek reikia mažiausiai traukimų, kad būtų galima teisingai sudėlioti etiketes. Argumentuoti.",
                       "1 traukimo. Traukiame iš „Obuoliai ir Apelsinai“, ištraukus apelsiną, čia bus „Apelsinai“. Tada lieka perkabinti dvi etiketės „Obuoliai ir Apelsinai“ ir „Obuoliai“. Žinome, kad obuolių indelyje negali būti obuoliai, todėl ten bus „Obuoliai ir Apelsinai“, paskutinis likęs indelis bus „Obuoliai“."),
                      ("Kaip perpjauti pyragą į 8 lygias dalis 3 pjūviais.",
                       "Per pusę, sudėti abi puses vieną ant kitos, kartoti dar du kartus arba supjausčius į keturias dalis, visus pjauti horizontaliai per vidurį."),
                      ("Du ąsočiai 4 ir 5 litrų talpos. Užduotis įpilti lygiai 7 litrus į kibirą. ",
                       "Pripilame 5 litrų ąsotį pilnai, nupilame 4 litrus į 4 litrų ąsotį, likusį litrą į kibirą, pakartoti dar vieną kartą, ir tada įpilti likusius 5 litrus."),
                      ("Mokslininkas augina bakteriją petri lėkštelėje. Kas valandą bakterija padvigubėja, po 17 valandų užima visą lėkštelę, po kiek valandų bakterija užėmė pusę indelio.",
                       "Kadangi dvigubėja, tai po 16 valandų t.y. prieš valandą."),
                      ("Koks stalo aukštis: <img src='static/stalas.JPG'>",
                       "Katė + Stalas = Vėžlys + 170cm | Vėžlys + Stalas = Katė + 130cm, sudedame abi lygtis ir išprastiname gyvūnus, gauname 2 Stalas = 300, tai Stalas = 150cm."),
                      ("Stovėjimo aikštelė sužymėta 16, 06, 68, 88, X, 98. Kokiu skaičiu pažymėtoje vietoje stovi mašina (X)?",
                       "Užduotis lengviau sprendžiama apvertus, seka nuo 86 iki 91, trūkstamas skaičius – 87."),
                      ("Turite 3 ir 5 litrų ąsočius, reikia išmatuoti 4 litrus vandens.",
                       "Pripilame pilną 5 litrų ąsotį. Perpilame 3 litrus į 3 litrų ąsotį, išpilame. Likusius du litrus perpilame į 3 litrų ąsotį. Prisipilame vėl 5 litrus į 5 litrų ąsotį, tada pilnai užpildome trijų litrų ąsotį, ten buvo likęs 1 litras tuščias, tada 5 litrų ąsotyje lieka 4."),
                      ("3x3 taškai, keturiomis tiesiomis linijomis, neatitraukiant rankos sujungti visus. <br> <img width=100px height=100px src='static/q7.jpg'/>",
                       "Vienas iš sprendimo variantų: <br> <img width=150px height=150px src='static/a7.jpg'>")]

    random_choice =  random.choice(questions_list)
    q = f"Klausimas: {random_choice[0]}"
    a = f"Atsakymas: {random_choice[1]}"


    return render_template('analysis_easy.html', title='Analitika lengvas', q=q, a=a)

@app.route("/draudimas_load")
def insurance_load():
    redirect_to = url_for('insurance')
    return render_template('loading.html', title='Kraunasi...', redirect=redirect_to)

@app.route("/draudimas")
def insurance():

    questions_list = [("'Gjensidige' logotipas - plačiai atpažįstamas saugumo simbolis Šiaurės šalyse. Kas jis?",
                       "Naktinis sargas."),
                      ("Gjensidige“ pradžia siejama su draudimo gaisro atvejais Land Gjensidige Brandkasse įsteigimu Oplando apskrityje, Norvegijoje. Kada tai įvyko?",
                       "Prieš 200 m. arba 1816 m."),
                      ("'Gjensidige' Lietuvoje prekiauja turto, kelionių, asmens, pirkinių, privalomojo vairuotojų ir kasko draudimais. Kokios rūšies tai draudimai?",
                       "Ne gyvybės draudimas."),
                      ("Norvegijoje „Gjensidige“ užima trečdalį visos ne gyvybės draudimo rinkos. Įmonė taip pat yra gerai žinoma ir vertinama klientų Baltijos šalyse. Tačiau, ką gi reiškia 'Gjensidige' pavadinimas?",
                       "Mutual arba abipusis."),
                      ("Draudimo bendrovės Lietuvoje siūlo platų draudimo produktų pasirinkimą - pradedant sveikatos baigiant turto draudimu, tačiau ne visi jie yra privalomi. Koks yra privalomas, o taip pat ir populiariausias, draudimo produktas Lietuvoje?",
                       "Transporto priemonių valdytojų civilinės atsakomybės / TPVCA / Vairuotojų civilinės atsakomybės."),
                      ("Paskolinote savo VW Golf automobilį draugui Marijui, tačiau jam vairuojant įvyko eismo įvykis, kurio metu Marijus sukdamas į kairę (degė žalias šviesoforo signalas) atsitrenkė į kito vairuotojo vairuojamą Fiat Multiplą, kuris važiavo tiesiai (degė žalias šviesoforo signalas). Vairuotojai sutarė draugiškai, nusprendė, kad Marijus yra kaltas dėl eismo įvykio ir supildė eismo įvykio deklaraciją. Ar jūsų privalomas vairuotojo draudimas padengs Fiat Multipla patirtus nuostolius eismo įvykio metu? Argumentuoti.",
                       "Taip, jeigu draudimo sąlygos nenurodo, kad transporto priemonės negali vairuoti kiti asmenys."),
                      ("Viduramžiais prekybininkai savo prekes siuntė jūra, kuomet kildavo įvairių pavojų. Prekybininkai naudojosi įvairiomis priemonėmis siekdami apsaugoti eksporto riziką. Užuot siuntę visas prekes viename laive, jie siuntė savo prekes per daug laivų, kad būtų išvengta visiško krovinio praradimo, jei laivą užklupo jūros audra, gaisras, piratai arba jis pateko į priešo išpuolius, tačiau tai nebuvo gera praktika dėl ilgo laiko ir skiriamų pastangų. Draudimas yra seniausias rizikos perkėlimo būdas, kuris buvo sukurtas siekiant sumažinti prekybos/ verslo riziką. Kokiame amžiuje ir šalyje buvo pasirašytas seniausias žinomas draudimo kontraktas?",
                       "XIV amžiaus vid., Italijoje."),
                      ("Ema savo namą apdraudė „Gjensidige“ būsto draudimu, kuris padengia daugiausia siūlomų būsto žalų, tarp jų ir namuose esančių namų apyvokos daiktų. Name taip pat yra garažas, kuriame Ema laiko savo automobilį. Deja, vieną vakarą namuose kilo gaisras. Name buvę žmonės nenukentėjo. Laimei, Ema buvo apdraudusi būstą, todėl namo atstatymo bei name sudegusių daiktų išlaidas draudimo bendrovė padengs. Tačiau sudegė ir name buvęs automobilis. Ar tokiu atveju „Gjensidige“ padengs patirtus nuostolius dėl sudegusio automobilio? Argumentuoti.",
                       "Ne, nes automobilis nepriklauso prie namų apyvokos daiktų."),
                      ("Andrius savo butą yra apdraudęs „Gjensidige“ būsto draudimo, kuris padengia daugiausia siūlomų būsto žalų, tarp jų ir namuose esančių namų apyvokos daiktų. Andrius yra išmanus, savo laiką vertinantis žmogus, todėl pavasario švarinimosi metu langų valymui naudojosi savo robotu langų valikliu. Robotas, bedirbdamas savo darbą iš išorinės lango pusės, atsikabino ir nukrito ant žemės. Deja, Andrius gyvena 12 aukšte ir jo robotas langų valiklis sudužo nebepataisomai. Ar tokiu atveju „Gjensidige“ padengs patirtus nuostolius dėl sudužusio roboto langų valiklio? Argumentuoti.",
                       "Taip, nes robotas valiklis yra namų apyvokos daiktas."),
                      ("Irenos kaimynas savo kieme augina aukštą klevą. Vienos itin stiprios audros metu medis užvirto ant Irenos namo. Kieno draudimas - Irenos ar jos kaimyno - turėtų padengti Irenos namo stogo taisymo išlaidas? Argumentuoti.",
                       "Irenos, jei ji yra apsidraudusi būsto draudimu.")]

    random_choice =  random.choice(questions_list)
    q = f"Klausimas: {random_choice[0]}"
    a = f"Atsakymas: {random_choice[1]}"

    return render_template('insurance.html', title='Draudimas', q=q, a=a)

@app.route("/rodyti_atsakyma")
def show_answer():
    a = request.args["a"]
    q = request.args["q"]
    return render_template('answer.html', title='Atsakymas', a=a, q=q)

@app.route('/mystery_box')
def mystery_box():
    return render_template('mystery_box.html', title='Mystery Box')

@app.route('/prizas')
def prize():
    prizes = firebase.get('', '')
    random_number = random.randint(0, len(prizes) - 1)

    prize_val = 0

    while prize_val == 0:
        prize = list(prizes.keys())[random_number]
        prize_val = prizes[prize]

    firebase.put('',
                 prize,
                 prize_val - 1)

    return render_template('prizas.html', title="Tavo prizas!", prize=prize)
