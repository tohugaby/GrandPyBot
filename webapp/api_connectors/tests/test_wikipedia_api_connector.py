"""
tests for wikipedia api connector
"""
import json
import requests_mock

from webapp.api_connectors.connectors import WikipediaApiConnector


@requests_mock.Mocker(kw="mock")
def test_wikipedia_api_return(**kwargs):
    """
    mock to test wikipedia api connector return
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "OpenClassrooms"
    api_connector_instance = WikipediaApiConnector(search_term)
    opensearch_url = api_connector_instance.get_search_url()
    search_url = api_connector_instance.get_search_url(query_term="OpenClassrooms")
    opensearch_results = ["OpenClassrooms", ["OpenClassrooms"], ["OpenClassrooms est une école en ligne"],
                          ["https://fr.wikipedia.org/wiki/OpenClassrooms"]]
    query_results = {
        'query': {
            'pages': {
                '4338589': {
                    'pageid': 4338589,
                    'ns': 0,
                    'title': 'OpenClassrooms',
                    'extract': '<p><b>OpenClassrooms</b> est une école en ligne...</p>'
                }
            }
        }
    }
    response = {
        'title': 'OpenClassrooms',
        'description': '<p><b>OpenClassrooms</b> est une école en ligne...</p>',
        'url': "https://fr.wikipedia.org/wiki/OpenClassrooms"
    }

    kwargs["mock"].get(opensearch_url, text=json.dumps(opensearch_results))
    kwargs["mock"].get(search_url, text=json.dumps(query_results))
    fake_results = api_connector_instance.search()
    assert fake_results == response
    assert isinstance(fake_results, dict)


@requests_mock.Mocker(kw="mock")
def test_wikipedia_api_empty_return(**kwargs):
    """
    mock to test wikipedia api connector return
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "ang"
    api_connector_instance = WikipediaApiConnector(search_term)
    opensearch_url = api_connector_instance.get_search_url()
    search_url = api_connector_instance.get_search_url(query_term="Ang")
    opensearch_results = ['ang',
                          ['Ang', 'Anglais', 'Angleterre', 'Anglicanisme', 'Angers', 'Angiosperme', 'Angelina Jolie',
                           'Angela Merkel', 'Angoulême', 'Angine'], ['',
                                                                     "L'anglais (English en anglais ; prononcé : /ˈɪŋ.ɡlɪʃ/) est une langue indo-européenne germanique originaire d'Angleterre qui tire ses racines de langues du nord de l'Europe (terre d'origine des Angles, des Saxons et des Frisons) dont le vocabulaire a été enrichi et la syntaxe et la grammaire modifiées par la langue normande apportée par les Normands, puis par le français avec les Plantagenêt.",
                                                                     "L'Angleterre (en anglais England) est une nation constitutive du Royaume-Uni  . Elle est bordée par l'Écosse au nord et le pays de Galles à l'ouest.",
                                                                     "L'anglicanisme est une confession chrétienne issue d'un schisme avec Rome en 1534, présente principalement dans les pays de culture anglophone, notamment dans toutes les anciennes colonies britanniques mais aussi sur les terres d'expatriation des Britanniques de par le monde.",
                                                                     "Angers (prononcer [ɑ̃ˑʒe] ) est une commune de l'Ouest de la France située au bord de la Maine, préfecture du département de Maine-et-Loire dans la région Pays de la Loire.",
                                                                     'La division des Angiospermes ou Magnoliophytes regroupe les plantes à fleurs, et donc les végétaux qui portent des fruits.',
                                                                     'Angelina Jolie, née Angelina Jolie Voight le 4 juin 1975 à Los Angeles, est une actrice, réalisatrice, scénariste, productrice, mannequin, philanthrope, écrivaine et ambassadrice de bonne volonté américano-cambodgienne.',
                                                                     "Angela Dorothea Merkel (API : /ˈaŋɡela doʀoˈteːa ˈmɛʁkl̩/), née Kasner le 17 juillet 1954 à Hambourg en Allemagne, est une femme d'État allemande, membre de l'Union chrétienne-démocrate (CDU) et chancelière fédérale depuis le 22 novembre 2005.",
                                                                     'Angoulême est une commune du Sud-Ouest de la France, préfecture du département de la Charente, en région Nouvelle-Aquitaine.',
                                                                     "L’angine et la pharyngite sont des infections aiguës de l'oropharynx, causées par des bactéries ou des virus."],
                          ['https://fr.wikipedia.org/wiki/Ang', 'https://fr.wikipedia.org/wiki/Anglais',
                           'https://fr.wikipedia.org/wiki/Angleterre', 'https://fr.wikipedia.org/wiki/Anglicanisme',
                           'https://fr.wikipedia.org/wiki/Angers', 'https://fr.wikipedia.org/wiki/Angiosperme',
                           'https://fr.wikipedia.org/wiki/Angelina_Jolie',
                           'https://fr.wikipedia.org/wiki/Angela_Merkel',
                           'https://fr.wikipedia.org/wiki/Angoul%C3%AAme', 'https://fr.wikipedia.org/wiki/Angine']]
    query_results = {'batchcomplete': '', 'warnings': {'extracts': {
        '*': '"exlimit" was too large for a whole article extracts request, lowered to 1.\nHTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats.'}},
                     'query': {'pages': {'4395334': {'pageid': 4395334, 'ns': 0, 'title': 'Ang', 'extract': ''}}}}

    response = {
        'title': 'Ang',
        'description': 'Désolé mon lapin , Je ne me souviens pas de Ang !',
        'url': "#"
    }

    kwargs["mock"].get(opensearch_url, text=json.dumps(opensearch_results))
    kwargs["mock"].get(search_url, text=json.dumps(query_results))
    fake_results = api_connector_instance.search()
    assert fake_results == response
    assert isinstance(fake_results, dict)


@requests_mock.Mocker(kw="mock")
def test_wikipedia_api_no_paragraph_return(**kwargs):
    """
    mock to test wikipedia api connector return
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "a"
    api_connector_instance = WikipediaApiConnector(search_term)
    opensearch_url = api_connector_instance.get_search_url()
    search_url = api_connector_instance.get_search_url(query_term="A")
    opensearch_results = ['a', ['A', 'Anglais', 'Allemagne', 'Aire (géométrie)', 'Animal', 'Australie',
                                "Autorité (sciences de l'information)", 'Altitude', 'Algérie', 'Angleterre'], [
                              "A ou a est la première lettre et la première voyelle de l'alphabet latin et de l'alphabet cyrillique.",
                              "L'anglais (English en anglais ; prononcé : /ˈɪŋ.ɡlɪʃ/) est une langue indo-européenne germanique originaire d'Angleterre qui tire ses racines de langues du nord de l'Europe (terre d'origine des Angles, des Saxons et des Frisons) dont le vocabulaire a été enrichi et la syntaxe et la grammaire modifiées par la langue normande apportée par les Normands, puis par le français avec les Plantagenêt.",
                              "L'Allemagne, en forme longue la République fédérale d'Allemagne abrégée en RFA (en allemand : Deutschland ; [forme longue] Bundesrepublik Deutschland, [abrégée en] BRD), est un pays d'Europe centrale, entouré par la mer du Nord, le Danemark et la mer Baltique au nord, par la Pologne et la République tchèque à l'est, par l'Autriche et la Suisse au sud, et par la France, le Luxembourg, la Belgique et les Pays-Bas à l'ouest.",
                              "En mathématiques, l'aire est une grandeur relative à certaines figures du plan ou des surfaces en géométrie dans l'espace.",
                              'Animalia',
                              "L'Australie, en forme longue le Commonwealth d'Australie (en anglais Australia et Commonwealth of Australia), est un pays de l'hémisphère sud dont la superficie couvre la plus grande partie de l'Océanie.",
                              "En science de l'information, une autorité (ou notice d'autorité ou forme d'autorité) sert à identifier sans ambiguïté des personnes, des choses ou des concepts.",
                              "L'altitude est l'élévation verticale d'un lieu ou d'un objet par rapport à un niveau de base. C'est une des composantes géographique et biogéographique qui explique la répartition de la vie sur terre.",
                              "L'Algérie (prononcé [al.ʒe.ˈʁi]  ; en arabe : الجزائر (al-Jazā'ir), ; en tamazight et arabe algérien : الدزاير (Dzayer), الجازاير (Djazaïr ou Jazaïr) ou لدزاير (Ldzayer) ; en tifinagh ⴷⵣⴰⵢⴻⵔ (dzayer)) est un pays d’Afrique du Nord faisant partie du Maghreb et, depuis 1962, un État nommé en forme longue la République algérienne démocratique et populaire, abrégée en RADP (en arabe الجمهورية الجزائرية الديمقراطية الشعبية ; en tamazight ⵜⴰⴳⴷⵓⴷⴰ ⵜⴰⵎⴻⴳⴷⴰⵢⵜ ⵜⴰⵖⴻⵔⴼⴰⵏⵜ ⵜⴰⴷⵣⴰⵢⵔⵉⵜ, Tagduda tamegdayt taɣerfant tadzayrit).",
                              "L'Angleterre (en anglais England) est une nation constitutive du Royaume-Uni  . Elle est bordée par l'Écosse au nord et le pays de Galles à l'ouest."],
                          ['https://fr.wikipedia.org/wiki/A', 'https://fr.wikipedia.org/wiki/Anglais',
                           'https://fr.wikipedia.org/wiki/Allemagne',
                           'https://fr.wikipedia.org/wiki/Aire_(g%C3%A9om%C3%A9trie)',
                           'https://fr.wikipedia.org/wiki/Animal', 'https://fr.wikipedia.org/wiki/Australie',
                           'https://fr.wikipedia.org/wiki/Autorit%C3%A9_(sciences_de_l%27information)',
                           'https://fr.wikipedia.org/wiki/Altitude', 'https://fr.wikipedia.org/wiki/Alg%C3%A9rie',
                           'https://fr.wikipedia.org/wiki/Angleterre']]

    query_results = {'batchcomplete': '', 'warnings': {'extracts': {
        '*': '"exlimit" was too large for a whole article extracts request, lowered to 1.\nHTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats.'}},
                     'query': {'pages': {'987086': {'pageid': 987086, 'ns': 0, 'title': 'A',
                                                    'extract': '<ul><li><b>A</b> ou <b>a</b> est la première lettre et la première voyelle de l\'alphabet latin et de l\'alphabet cyrillique.</li>\n<li><b>A</b> est la majuscule de\xa0:\n<ul><li><b>a</b>, lettre de l\'alphabet latin et de l\'alphabet cyrillique\xa0;</li>\n<li>α (alpha), lettre de l\'alphabet grec.</li>\n</ul></li>\n<li>La lettre <b>A</b> ou <b>a</b> est employée isolément dans divers contextes.</li>\n</ul><p></p>\n\n<p></p>\n<h2><span id="Arts_et_culture">Arts et culture</span></h2>\n<h3><span id="Litt.C3.A9rature"></span><span id="Littérature">Littérature</span></h3>\n<ul><li><i>Cycle du Ā</i> (ou <i>du non-A</i>), une série de romans de science-fiction écrits par A. E. van Vogt\xa0;</li>\n<li><i>Le Naufragé du « A »</i>, un album de l’auteur de bande dessinée Fred (cycle de Philémon)\xa0;</li>\n<li><i>A</i> est le nom du <i><abbr class="abbr" title="Cinquième">5<sup>e</sup></abbr> Raikage</i> dans le manga <i>Naruto</i>\xa0;</li>\n<li>La Lettre A, le titre d\'une «\xa0lettre confidentielle\xa0» destinée aux décideurs français.</li>\n<li>-A fait aussi référence au(x) personnage(s) qui persécute les personnages des livres et de la série Pretty Little Liars diffusée sur ABC family.</li>\n<li><b>A</b> et <b><span>B</span></b> sont les protagonistes du <i>Supplément au voyage de Bougainville</i> de Denis Diderot.</li>\n<li><b>"A"</b> est l\'antagoniste principal de la série télévisée <i>Pretty Little Liars</i> et de la série littéraire Les Menteuses, de Sara Shepard, dont elle est issue.</li>\n</ul><h3><span id="Musique">Musique</span></h3>\n<ul><li>A, la note <i>la</i> employée dans les pays qui utilisent des lettres de l’alphabet pour nommer les notes de musique.</li>\n<li>A, l’abréviation du mot alto\xa0;</li>\n<li>A, un groupe de musique de genre nu metal.</li>\n</ul><h4><span id="Album">Album</span></h4>\n<ul><li><i>A</i>, un album de musique du groupe Jethro Tull de 1980\xa0;</li>\n<li><i>A</i>, le titre d\'un single de Ayumi Hamasaki.</li>\n</ul><h2><span id="Science_et_technique">Science et technique</span></h2>\n<h3><span id="Biologie">Biologie</span></h3>\n<ul><li>Groupe A, un groupe sanguin de l’Homme\xa0;</li>\n<li>Protéine A, protéine de la paroi de la Bactérie <i>Staphylococcus aureus</i>, affine du fragment Fc des immunoglobulines <i>;</i></li>\n<li>Strie A, abréviation de strie anistropique\xa0;</li>\n<li>Site A, site ribosomique\xa0;</li>\n<li>Vitamine A, un type de vitamine\xa0;</li>\n<li>A, l’adénine dans la transcription d\'une chaîne d’ADN ou d’ARN, une des bases azotées puriques\xa0;</li>\n<li>A, l\'alanine dans la transcription d\'une chaîne polypeptidique.</li>\n<li>A, l\'adénosine, nucléoside constitutif des nucléotides et des acides nucléiques\xa0;</li>\n<li>A, l\'adénylate (ou adénosine-5\'-mono-phosphate) dans la séquence des acides nucléiques\xa0;</li>\n<li>A, symbole des nervures anales des ailes d\'Insectes, dans le système Comstock-Needham (1898)\xa0;</li>\n<li>A, symbole de l\'absorbance\xa0;</li>\n<li>a, symbole du sang artériel\xa0;</li>\n<li>a, symbole de l\'air alvéolaire\xa0;</li>\n</ul><h3><span id="Calendriers">Calendriers</span></h3>\n<ul><li><i>a</i> (du latin <i>annus</i>) est utilisé comme symbole de l’année civile.</li>\n<li>A<i>, la lettre dominicale représentant une année commune commençant un dimanche et comportant donc 52 semaines. Dans le calendrier grégorien,</i></li>\n</ul><h3><span id="Math.C3.A9matiques"></span><span id="Mathématiques">Mathématiques</span></h3>\n<ul><li><span><span><math xmlns="http://www.w3.org/1998/Math/MathML" alttext="{\\displaystyle \\ A}">\n  <semantics>\n    <mrow class="MJX-TeXAtom-ORD">\n      <mstyle displaystyle="true" scriptlevel="0">\n        <mtext>\xa0</mtext>\n        <mi>A</mi>\n      </mstyle>\n    </mrow>\n    <annotation encoding="application/x-tex">{\\displaystyle \\ A}</annotation>\n  </semantics></math></span></span> désigne une aire\xa0;</li>\n<li><span><span><math xmlns="http://www.w3.org/1998/Math/MathML" alttext="{\\displaystyle A_{n}^{k}}">\n  <semantics>\n    <mrow class="MJX-TeXAtom-ORD">\n      <mstyle displaystyle="true" scriptlevel="0">\n        <msubsup>\n          <mi>A</mi>\n          <mrow class="MJX-TeXAtom-ORD">\n            <mi>n</mi>\n          </mrow>\n          <mrow class="MJX-TeXAtom-ORD">\n            <mi>k</mi>\n          </mrow>\n        </msubsup>\n      </mstyle>\n    </mrow>\n    <annotation encoding="application/x-tex">{\\displaystyle A_{n}^{k}}</annotation>\n  </semantics></math></span></span> désigne un arrangement\xa0;</li>\n<li>Nombre A correspond à la valeur 10 (en décimal) dans le système hexadécimal (base 16)\xa0;</li>\n</ul><h3><span id="Phon.C3.A9tique"></span><span id="Phonétique">Phonétique</span></h3>\n<ul><li>[a] est le symbole de l\'alphabet phonétique international qui représente la voyelle ouverte antérieure non-arrondie.</li>\n<li>[ɐ] est le symbole de l\'alphabet phonétique international qui représente la voyelle pré-ouverte centrale.</li>\n</ul><h3><span id="Physique_-_Chimie">Physique - Chimie</span></h3>\n<ul><li><b>a</b>, la diffusivité thermique\xa0;</li>\n<li><b>a</b>, l\'activité chimique d\'un composant\xa0;</li>\n<li><b>A</b>, une classe d’étoiles déterminée par leur type spectral\xa0;</li>\n<li><b>A</b> (cursif) désigne l\'affinité chimique\xa0;</li>\n<li><b>A</b>, une notation rare de l\'enthalpie libre (énergie de Gibbs)\xa0;</li>\n<li><b>A</b>, le nombre de masse, égal au nombre de nucléons de l\'atome, placé en haut et à gauche du symbole\xa0;</li>\n<li>Bombe A, une bombe nucléaire à fission.</li>\n</ul><h3><span id="Psychanalyse">Psychanalyse</span></h3>\n<ul><li>L’objet a désigne, chez Jacques Lacan, l\'objet du désir.</li>\n</ul><h3><span id="Unit.C3.A9s"></span><span id="Unités">Unités</span></h3>\n<ul><li>a, un préfixe du Système international d\'unités signifiant atto (10<sup>-18</sup>)\xa0;</li>\n<li>a, le symbole de l’are, unité de mesure d’une superficie\xa0;</li>\n<li>A, le symbole de l\'ampère dans le système international d\'unités\xa0;</li>\n<li>Å, le symbole de l’ångström.</li>\n</ul><h2><span id="Toponyme">Toponyme</span></h2>\n<ul><li><span>Å</span>, le nom de plusieurs localités scandinaves\xa0;</li>\n<li>Aa, un petit fleuve côtier français du nord de la France, dans la région Nord-Pas-de-Calais\xa0;</li>\n<li>Famille d\'Aa, famille de notables du Duché de Brabant entre les <abbr class="abbr" title="11ᵉ siècle"><span>XI</span><sup style="font-size:72%">e</sup></abbr> et <abbr class="abbr" title="14ᵉ siècle"><span>XIV</span><sup style="font-size:72%">e</sup></abbr>\xa0siècles.</li>\n<li>L\'aiguille de l\'A Neuve est un sommet du massif du Mont-Blanc.</li>\n</ul><h2><span id="Autres">Autres</span></h2>\n<ul><li><i>A</i>, l\'abréviation latine du prénom Aulus\xa0;</li>\n<li><i>A</i> entourée d\'un rond est un symbole des anarchistes\xa0;</li>\n<li>Ā (阿), un idéogramme chinois traduit en hanyu pinyin\xa0;</li>\n<li>Formats A, différents formats de papier.</li>\n<li>A, un méga-yacht de 118\xa0mètres, propriété du russe Andrey Melnichenko</li>\n<li>En France, A majuscule inscrit en rouge sur un disque blanc est le signe distinctif qui doit être apposé à l\'arrière d\'un véhicule conduit par un élève conducteur ou par un conducteur ayant obtenu son permis depuis moins de 3 ans, ou depuis moins de 2 ans s\'il a bénéficié de la conduite accompagnée (articles L223-1 et R413-5 du code de la route).</li>\n<li>"A" vient du verbe "avoir" conjugé à la troisieme personne du singulier au présent de l\'indicatif.</li>\n</ul><h2><span id="Notes_et_r.C3.A9f.C3.A9rences"></span><span id="Notes_et_références">Notes et références</span></h2>'}}}}

    response = {
        'title': 'A',
        'description': """A ou a est la première lettre et la première voyelle de l'alphabet latin et de l'alphabet cyrillique.A est la majuscule de :a, lettre de l'alphabet latin et de l'alphabet cyrillique ;α (alpha), lettre de l'alphabet grec.La lettre A ou a est employée isolément dans divers contextes.Arts et cultureLittératureCycle du Ā (ou du non-A), une série de romans de science-fiction écrits par A. E. van Vogt ;...""",
        'url': "https://fr.wikipedia.org/wiki/A"
    }

    kwargs["mock"].get(opensearch_url, text=json.dumps(opensearch_results))
    kwargs["mock"].get(search_url, text=json.dumps(query_results))
    fake_results = api_connector_instance.search()
    assert fake_results == response
    assert isinstance(fake_results, dict)
