# obfusqf-deobf

Déobfuscateur pour les missions Arma 3 protégées par **ObfuSQF**, basé sur le
schéma décrit dans le document public « Hallo i bims der Deobfuscator ».

## Version web (sans installation)

`web/index.html` est un outil **100 % client** (un seul fichier, aucune
 dépendance) : ouvre-le dans un navigateur, colle le code obfusqué ou
 glisse-dépose des fichiers, et obtiens le rapport (clés, chemins aléatoires,
 signaux) + le code recollé. Pour l'héberger gratuitement : GitHub →
 *Settings → Pages* → branche `main`, dossier `/web`.

- la **clé** est stockée en clair dans la mission (fichier `*.rsa.sqf`, ou
  garde `loadFile "...rsa.sqf") find "CLÉ" == -1` dans la fonction compilée) ;
- les chaînes sont **découpées en petits chunks** recollés avec `+` (ou `/`)
  pour donner une impression de sécurité ;
- les chemins de chargement utilisent des **arborescences de dossiers
  aléatoires** sous `ObfuSQF\`.

## Installation

Python 3.10+, aucune dépendance runtime (pytest uniquement pour les tests).

```bash
pip install pytest        # optionnel, pour les tests
python -m pytest tests/ -q
```

## Utilisation

```bash
# Scanner une mission / un mod et détecter les traces ObfuSQF
python -m obfusqf_deobf scan <dossier_mission>

# Extraire toutes les clés trouvées (fichiers rsa.sqf + gardes dans le code)
python -m obfusqf_deobf keys <dossier_mission>

# Déobfusquer un fichier .sqf (ou stdin avec -)
python -m obfusqf_deobf deobfuscate function.sqf
python -m obfusqf_deobf deobfuscate - --json < function.sqf

# Lire un fichier .sqf avec numéros de ligne (--no-numbers pour brut, --json)
python -m obfusqf_deobf read function.sqf
```

### Exemple

```
$ python -m obfusqf_deobf deobfuscate samples/obfuscated_function.sqf
obfuscated: yes
split-string sequences merged: 41
key (loadFile ObfuSQF\...rsa.sqf): ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir
--- deobfuscated code ---
[]call compile('if(isServer)exitWith();if((loadFile "ObfuSQF\...rsa.sqf") find "ZP7..." == -1)then(...');
```

## Limites connues

- L'outil recolle les chaînes et extrait les clés ; il ne déchiffre pas le
  contenu des `.sqf` protégés par la clé (le schéma ObfuSQF documenté ne fait
  qu'une comparaison de clé, pas un vrai chiffrement).
- Un `'+'` ou `'/'` légitime *entre* deux littéraux dans du SQF honnête peut
  être fusionné par erreur — vérifier la sortie avant utilisation.

## Structure

```
obfusqf_deobf/
  strings.py       recollage des littéraux découpés
  keys.py          extraction des clés (rsa.sqf + gardes loadFile/find)
  scanner.py       scan d'arborescence + rapport
  deobfuscate.py   pipeline haut niveau
  cli.py           interface en ligne de commande
tests/             pytest
samples/           mission d'exemple obfusquée (données du document source)
```
