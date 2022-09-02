# Copilot Benchmark

Platefrome pour tester les complétions de Github Copilot et Codex.

## Installation

### Installation d'un virtualenv

```bash
python -m venv venv
source venv/bin/activate
```

### Installation de Copilot et des dépendances

```bash
pip install -r requirements.txt
pip install -e .
```

Pour activer copilot il faut installer le plugin copilot sur neovim et se connecter à github avec.

## Usage

Les scripts de génération et de test sont disponibles dans le dossier `humaneval` et `leetcode`.
Pour obtenir les paramètres de génération, utiliser le flag `--help`.

Le notebook `results.ipynb` permet de visualiser et utiliser les résultats des tests. Les résultats brut sont disponibles dans les dossier `humaneval` et `leetcode` sous le nom `results.json`.

Le dossier `copilot` contient le package permettant d'utiliser copilot.

Le dossier `utils` contient des fonctions utiles pour la génération de code et les tests.
