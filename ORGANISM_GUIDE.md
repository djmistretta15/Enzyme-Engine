# 🌍 Universal Organism Guide

The Enzyme Discovery System is **not limited to the Emerald Ash Borer** — it's a universal platform that can discover enzymes in **any organism** with sequences in NCBI databases.

## 🚀 Quick Start with Different Organisms

### Pre-Configured Profiles

```bash
# Emerald Ash Borer (wood-boring beetle)
python discover.py eab --max-results 200

# Termites (with symbiotic gut microbiome)
python discover.py termite --enzyme cellulase --max-results 150

# Bark Beetles (fungal symbionts)
python discover.py bark-beetle --max-results 100

# Wood-Rot Fungi (nature's lignin destroyers)
python discover.py fungus --enzyme laccase --max-results 200

# Any Custom Organism
python discover.py custom --organism "Teredo navalis" --max-results 100
```

### Using Original CLI

```bash
# Just change the --organism parameter!
python main.py --organism "Reticulitermes flavipes" --max-results 200
python main.py --organism "Dendroctonus ponderosae" --enzyme cellulase
python main.py --organism "Phanerochaete chrysosporium" --database protein
```

## 🐛 Organism Examples by Category

### Wood-Degrading Insects

| Organism | Common Name | Why Interesting |
|----------|-------------|-----------------|
| *Agrilus planipennis* | Emerald Ash Borer | Devastating invasive beetle |
| *Reticulitermes flavipes* | Eastern Subterranean Termite | Symbiotic gut protozoa |
| *Dendroctonus ponderosae* | Mountain Pine Beetle | Fungal symbionts, forest pest |
| *Anoplophora glabripennis* | Asian Longhorned Beetle | Invasive hardwood borer |
| *Teredo navalis* | Shipworm | Marine wood borer (mollusk!) |
| *Sirex noctilio* | Sirex Woodwasp | Fungal symbiont system |

**Example:**
```bash
python discover.py custom --organism "Anoplophora glabripennis" --max-results 150
```

### Termites & Social Insects

| Organism | Common Name | Special Features |
|----------|-------------|------------------|
| *Reticulitermes flavipes* | Eastern Subterranean Termite | Gut flagellates |
| *Coptotermes formosanus* | Formosan Termite | Highly destructive |
| *Zootermopsis angusticollis* | Pacific Dampwood Termite | Large gut microbiome |
| *Nasutitermes corniger* | Nasute Termite | Fungus-growing |

**Example:**
```bash
python discover.py termite --enzyme cellulase --max-results 200
```

### Fungi (White-Rot & Brown-Rot)

| Organism | Type | Lignin Degradation |
|----------|------|-------------------|
| *Phanerochaete chrysosporium* | White-rot | Lignin peroxidases |
| *Trametes versicolor* | White-rot | High laccase activity |
| *Pleurotus ostreatus* | White-rot | Edible, versatile |
| *Postia placenta* | Brown-rot | Fenton chemistry |
| *Gloeophyllum trabeum* | Brown-rot | Non-enzymatic pathway |

**Example:**
```bash
python discover.py fungus --enzyme peroxidase --max-results 250
```

### Bacteria (Cellulolytic)

| Organism | Environment | Applications |
|----------|-------------|--------------|
| *Clostridium thermocellum* | Anaerobic, thermophilic | Biofuel production |
| *Cellulomonas fimi* | Soil bacterium | Industrial enzymes |
| *Cellvibrio japonicus* | Soil bacterium | Biomass degradation |
| *Ruminococcus flavefaciens* | Rumen | Animal digestion |

**Example:**
```bash
python main.py --organism "Clostridium thermocellum" --enzyme cellulase --max-results 100
```

### Marine Wood Borers

| Organism | Common Name | Unique Features |
|----------|-------------|-----------------|
| *Teredo navalis* | Common Shipworm | Mollusk with bacterial symbionts |
| *Limnoria quadripunctata* | Gribble | Crustacean wood borer |
| *Chelura terebrans* | Marine amphipod | Cellulose digestion |

**Example:**
```bash
python main.py --organism "Teredo navalis" --database protein --max-results 150
```

## 🧪 Non-Wood Applications

### Chitin Degraders
```bash
# Crab shell decomposers
python main.py --organism "Serratia marcescens" --max-results 100
```

### Keratin Degraders
```bash
# Feather/hair decomposers
python main.py --organism "Streptomyces fradiae" --max-results 100
```

### Plastic Degraders
```bash
# PET-eating bacteria
python main.py --organism "Ideonella sakaiensis" --max-results 100
```

### Oil Degraders
```bash
# Bioremediation
python main.py --organism "Alcanivorax borkumensis" --max-results 100
```

## 🔬 How to Discover Enzymes in a New Organism

### Step 1: Check if it's in NCBI

Visit [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) and search for your organism.

### Step 2: Run Discovery

```bash
python discover.py custom --organism "Your Organism Name" --max-results 200
```

### Step 3: Review Results

Check `backend/data/results/` for:
- `digestive_matrix.csv` - Top enzyme candidates
- `discovery_report.txt` - Detailed analysis
- Visualization PNGs

### Step 4: Customize (Optional)

Create a config file in `backend/organism_configs/` for your organism if you plan to use it repeatedly.

## 📊 What Gets Discovered

For **any organism**, the system finds:

✅ **Cellulases** (GH5, GH6, GH7, GH9, GH45, GH48)
✅ **Laccases** (AA1)
✅ **Peroxidases** (AA2)
✅ **Oxidases** (AA3, AA4)
✅ **Xylanases** (GH10, GH11)
✅ **β-glucosidases** (GH1, GH3)
✅ **Mannanases** (GH26)
✅ **ANY enzyme with EC numbers or GH families**

## 🌐 Cross-Species Comparisons

You can compare enzyme repertoires across species:

```bash
# Run discovery for multiple organisms
python discover.py eab --max-results 200
python discover.py bark-beetle --max-results 200
python discover.py termite --max-results 200

# Then compare the digestive_matrix.csv files
```

## 🧬 Research Applications

### Comparative Genomics
Compare wood-digesting systems across:
- Insects vs. Fungi vs. Bacteria
- Related beetle species
- Invasive vs. native species

### Biotech Applications
- **Biofuel production** - thermophilic bacteria
- **Industrial enzymes** - fungal laccases
- **Biomass conversion** - termite symbionts
- **Bioremediation** - plastic/oil degraders

### Evolutionary Biology
- Horizontal gene transfer in insects
- Convergent evolution of cellulases
- Symbiont-host coevolution

## 🎯 Tips for Success

### 1. **Start Broad**
```bash
# Get all enzymes first
python main.py --organism "Your Organism" --max-results 200
```

### 2. **Then Narrow Down**
```bash
# Focus on specific enzyme type
python main.py --organism "Your Organism" --enzyme cellulase --max-results 100
```

### 3. **Use Related Species**
Edit `config.py` to add related species for cross-species discovery.

### 4. **Check Multiple Databases**
```bash
# Proteins
python main.py --organism "Your Organism" --database protein

# Nucleotides (genes)
python main.py --organism "Your Organism" --database nucleotide

# Transcriptomes
python main.py --organism "Your Organism" --database sra
```

## 🔧 Creating Custom Organism Profiles

See examples in `backend/organism_configs/`:
- `termite_config.py` - Gut symbiont focus
- `bark_beetle_config.py` - Fungal symbiont focus
- `fungal_config.py` - Extracellular enzyme focus

Copy and modify for your organism!

## 💡 Example Workflows

### Discover Termite Gut Enzymes
```bash
python discover.py termite --max-results 250
# Results show symbiont-derived cellulases
```

### Find Fungal Lignin Peroxidases
```bash
python discover.py fungus --enzyme peroxidase --max-results 200
# Results ranked by lignin-degrading potential
```

### Screen Shipworm Cellulases
```bash
python discover.py custom --organism "Teredo navalis" --enzyme cellulase --max-results 150
# Results show marine-adapted enzymes
```

### Compare Bark Beetle Detox Enzymes
```bash
python discover.py bark-beetle --max-results 200
# Results include cytochrome P450s for terpene detoxification
```

## 🌍 The Bottom Line

**This platform works for ANY organism with genomic/transcriptomic data in NCBI.**

Whether you're studying:
- 🪲 Beetles
- 🦗 Termites
- 🍄 Fungi
- 🦠 Bacteria
- 🐚 Shipworms
- 🧫 Anything else!

Just change the organism name, and the entire pipeline adapts automatically.

---

**Ready to discover enzymes in your organism of interest?**

```bash
python discover.py --list  # See all pre-configured profiles
python discover.py custom --organism "Your Favorite Organism" --max-results 200
```
