# -*- coding: utf-8 -*-
"""Génère la traduction française du PDF « Hallo i bims der Deobfuscator »."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

IMG = Path("/workspace/.vibe/tool-results/ocr/9b61098df9e731a647f1fc1bd719cc9838329240a3d6604f9ae106ef701eab00/images")
OUT = Path(__file__).resolve().parent.parent / "docs" / "Hallo-i-bims-der-Deobfuscator-FR.pdf"

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=8)
title = ParagraphStyle("title", parent=body, fontSize=13, spaceAfter=12)
code = ParagraphStyle("code", fontName="Courier", fontSize=7.2, leading=9.2, backColor="#f2f2f2", borderPadding=4, spaceAfter=10)
center = ParagraphStyle("center", parent=body, alignment=1)
h2 = ParagraphStyle("h2", parent=body, fontSize=12, spaceBefore=6, spaceAfter=10)
body3 = ParagraphStyle("body3", parent=body, fontSize=9.3, leading=12.6, spaceAfter=4)
code3 = ParagraphStyle("code3", parent=code, fontSize=6.8, leading=8.4, borderPadding=2, spaceAfter=6)


def img(name, width):
    path = IMG / name
    from PIL import Image as PILImage

    w, h = PILImage.open(path).size
    return Image(str(path), width=width, height=width * h / w)


story = []

# ---- Page 1 ----
story.append(Paragraph("Salut, c'est le Deobfuscateur qui vous parle,", title))
story.append(Paragraph(
    "Bon, mesdames et messieurs, aujourd'hui nous allons vous montrer à quel point "
    "Maverick-Apps est « sécurisé ». Nous avons consacré environ 2 heures ± 30 minutes "
    "(pause déjeuner comprise) à cet outil, avant de devoir constater que nous avions "
    "déjà tout percé.", body))
story.append(img("page-0001-image-0001.jpg", 10 * cm))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Blague à part, on a presque pleuré tellement c'était simple. Personnellement, "
    "j'en avais les larmes aux yeux (si vous voyez ce que je veux dire) quand j'ai vu "
    "à quel point c'était facile, mais bon.", body))
story.append(Paragraph(
    "Je me souviens de discussions avec les créateurs de cet outil « glorieux » et "
    "« sécurisé » : ils prétendaient qu'il était quasiment impossible d'accéder aux "
    "fichiers ou à la clé. Mais bon…", body))
story.append(img("page-0001-image-0002.jpg", 6 * cm))
story.append(Spacer(1, 8))
story.append(Paragraph("Bon, assez de memes, passons à la suite.", body))
story.append(PageBreak())

# ---- Page 2 ----
story.append(Paragraph(
    "<b>Comment fonctionne ce chiffrement ?</b> Eh bien, tout d'abord — et c'est là le "
    "point clé, accrochez-vous — la CLÉ !!! est stockée dans la mission. Autrement dit, "
    "il suffit d'ouvrir la mission avec l'éditeur de texte de notre choix : Notepad++ "
    "dans ce cas. Tout paraît un peu confus au premier abord, mais on trouve la clé si "
    "l'on sait quoi chercher.", body))
story.append(Paragraph(
    "<b>Note en marge : Obfuscation = STUPIDE.</b> Pourquoi, vous demandez-vous ? Eh "
    "bien, il faut bien stocker la clé, même si elle est aléatoire — mais elle figure "
    "donc quand même dans la mission = STUPIDE", body))
story.append(Paragraph(
    "Continuons. Voici comment nous avons procédé : d'abord nous avons bloqué "
    "<b>preprocessFile</b>, puis nous avons extrait les fonctions MAV_Sub_ / "
    "mav_tag_fnc_* avec le Config Viewer.", body))
story.append(Paragraph("<i>Le nom de la fonction peut différer de l'exemple.</i>", body))
story.append(Paragraph("Quand on exécute cette fonction, on obtient quelque chose dans ce genre :", body))
story.append(Preformatted("""[]call compile('i'+'f('+'isS'+'erver)exi'+'tWit'+'h{);if((lo'+'adF'+'ile
"O'+'bf'+'uS'+'Q'+'F'if6a0hbysx7'nxlorxzekp\\id2drwzwzx\\9dr1dxgzph.rs'/'a.sq'/'f" fi'/'nd
"AoGADbTEoVY5U7a9RfznojcsyVExOWUEyv9Aj1LTCpdZiYjfh9p09BHwSMdEJRr3" = '+'= -1)th'/'en(pre'/'proc'/'essFi'/'le
"CPIPT\\KOILM\\KONV5\\SETTM\\PTN0I.sqf';[''] ex'/'ec'/'VM
"CPIPT\\KOILM\\KONV5\\SETTM\\PTN0I.sqf';['']spa'/'wn{w'/'hile{tr'/'ue}d'/'o'/'{"Ev'/'ery'/'one'/'Los'/'t' ca'/'ll
BI'/'S'/'_f'/'nc'/'_en'/'d'/'Mis'/'sio'/'nSe'/'rver;{';'};'};'};'""", code))
story.append(Paragraph(
    "Comme on le voit, les chaînes sont joliment découpées avec des + pour donner une "
    "impression « plus sécurisée ».", body))
story.append(Preformatted("""[]call compile(
    'i'+'f('+'isS'+'erver)exi'+'tWit'+'h();
    if((lo'+'adF'+'ile "O'+'bf'+'uS'+'Q'+'F'+'pjjboo0shh\\arrdyhg2n3\\wqdbfn113f\\lcmixn5bwv\\slgpvk8qzo\\ec1utgmpks\\swhieoq8fz\\pslnmmw1wr.rs'+'a.sq'+'f") fi'+'nd
    "ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir") = '+'= -1)th'+'en(
    pre'+'proc'+'essFi'+'le "VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf";
    [''] ex'+'ec'+'VM "VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf";
    ['']spawn(
    while{true}do{
    "EveryoneLost" call BIS_fnc_endMissionServer;
    );
    ');
    ');
    ');
if(!isServer) exitWith ();
if((loadFile "ObfuSQF\\pjjboo0shh\\arrdyhg2n3\\wqdbfn113f\\lcmixn5bwv\\slgpvk8qzo\\ec1utgmpks\\swhieoq8fz\\pslnmmw1wr.rs.sqf") find
    "ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir") == -1) then (
    preprocessFile "VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf";
    [] execVM "VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf";
    [] spawn (
    while (true) do (
    "EveryoneLost" call BIS_fnc_endMissionServer;
    );
);""", code))
story.append(Paragraph("<b>Encore une fois, pour ceux qui ont une mauvaise vue : voir l'image.</b>", body))
story.append(Paragraph("\\_(ツ)_/ Tutoriel à la page suivante ! \\_(ツ)_/", center))
story.append(PageBreak())

# ---- Page 3 ----
story.append(Paragraph("<b>Que dois-je faire maintenant ?</b>", body3))
story.append(Paragraph(
    "1. Récupérer la mission depuis %appdata% et l'installer sur un serveur de test local.", body3))
story.append(Paragraph(
    "2. Modifier le fichier server.cfg :<br/>"
    "&nbsp;&nbsp;&nbsp;<font face='Courier'>allowedPreprocessFileExtensions[] = {\"\"};</font><br/>"
    "Ainsi, le serveur ne plante pas, mais les fonctions du Functions.hpp ne sont pas "
    "non plus chargées. Il faudra annuler cette modification après avoir effectué les "
    "étapes suivantes et créé la mod serveur.", body3))
story.append(Paragraph("3. Créer une mod serveur nommée : @ObfuSQF", body3))
story.append(Paragraph(
    "4. Dans cette mod, créer un répertoire avec les sous-répertoires indiqués "
    "ci-dessus. Le chemin doit ressembler à ceci :<br/>"
    "&nbsp;&nbsp;&nbsp;<font face='Courier'>\\ObfuSQF\\pjjboc0shh\\arrdyhq2m3\\wgdbfm113f\\cmixm5bwv\\slgpvk8qzo\\ec1utgmpks\\swhieoq8fz\\pslnmmw1wr.rsa.sqf\"</font><br/>"
    "<i>Remarque : pourquoi autant de dossiers ? Maverick pense que ça rend le tout "
    "« plus sécurisé ».</i>", body3))
story.append(Paragraph(
    "5. Le fichier rsa.sqf doit contenir ceci : "
    "<font face='Courier'>\"XP7CZIIMRI39P9fsyJbhMpYFG0Odff7V4m+essA09hir\"</font><br/>"
    "<i>Il est toujours différent.</i>", body3))
story.append(Paragraph(
    "6. Packager le tout en mod, lancer un serveur avec la ObfuSQF.pbo — vous pourrez "
    "alors simplement rejoindre la mission et lire et utiliser chaque fonction. "
    "Éventuellement, on peut aussi utiliser un script qui, via des DLL comme "
    "KK_makefile.dll, écrit automatiquement tous les scripts dans le répertoire racine "
    "d'Arma 3.", body3))
story.append(Paragraph(
    "<b>Remarque :</b> si quelqu'un dit « je n'arrive pas à ouvrir la console de "
    "debug », il existe plein de mods qui résolvent ce problème. #NSS Adminmenu", body3))
story.append(Paragraph("Il n'y a fondamentalement rien de plus à en dire.", body3))
story.append(Paragraph("<b>Voici quelques clés :</b>", body3))
story.append(Paragraph("Mission SAMPLE :", body3))
story.append(Preformatted("+gc25l47UWKtTwDXDvBMVIII9p4q9rXGxSXJWUZ/IoWGJe+QDYu+cMtyVUlyPhMyF", code3))
story.append(Paragraph("Eisenschmiede :", body3))
story.append(Preformatted("XP7CZIIMRI39P9fsyJbhMpYFG0Odff7V4m+essA09hir", code3))
story.append(Paragraph("LiveYourLife :", body3))
story.append(Preformatted("Ancienne clé : AoGADbTEoVY5U7a9RfznojcsyVExOWUEyv9Aj1LTCpdZiYjfh9p09BHwSMdEJRr3", code3))
story.append(Paragraph(
    "Spécialement pour Crackihead, la nouvelle clé :D HF (bon courage !)", body3))
story.append(Paragraph(
    "La nouvelle arborescence de dossiers : "
    "<font face='Courier'>8kcksptdvq\\wzcottozge\\rwinhljmlk\\eqcf1ipasm\\swpyrge9vp\\</font>", body3))
story.append(Paragraph("Le fichier s'appelle : <font face='Courier'>5wjmp5pddw.rsa.sqf</font>", body3))
story.append(Paragraph("avec la clé suivante :", body3))
story.append(Preformatted('"QR37d2qc2ToYlhU1LpUTBWNGa5wzfyIE+4yhgpCr3u1L5X2+iXr87Wloxmoqyyk/"', code3))
story.append(Paragraph("Le modifier ne sert de toute façon à rien, donc laisse tomber :)", body3))
story.append(Paragraph("Le contenu SQF appartient à tout le monde, alors laisse-le en place !", body3))
story.append(Paragraph(
    "Laisse donc les crédits des personnes qui créent les scripts, et tout ira bien — "
    "c'est comme ça que tout le monde devrait faire !", body3))
story.append(Paragraph("GrandTheftArma :", body3))
story.append(Preformatted("BISz3LQo69/68ThbhS+ZokCxySydj4rXgHB78QTjeNOCDRyAteY/hGiAJWTF2ufT", code3))
story.append(PageBreak())

# ---- Page 4 ----
story.append(Paragraph("## Perte de temps", h2))
story.append(img("page-0004-image-0001.jpg", 12 * cm))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Merci de votre attention, et merci de ne pas flammer (troller),", body))
story.append(Paragraph("Voici la licorne anti-rage :", body))
story.append(img("page-0004-image-0002.jpg", 7 * cm))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Cordialement, ImSorry</b>", body))
story.append(PageBreak())
story.append(Spacer(1, 1))

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUT), pagesize=A4, topMargin=1.8 * cm, bottomMargin=1.8 * cm, leftMargin=2 * cm, rightMargin=2 * cm, title="Hallo i bims der Deobfuscator — Traduction FR")
doc.build(story)
print("PDF généré :", OUT)
