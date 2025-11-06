"""
Visualization Module
Generate charts and plots for enzyme data analysis
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import pandas as pd
from typing import Dict, List, Optional
import logging
from pathlib import Path

from ..config import CHART_COLORS, RESULTS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnzymeVisualizer:
    """Create visualizations for enzyme discovery data"""

    def __init__(self, output_dir: str = RESULTS_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = CHART_COLORS

    def plot_enzyme_distribution(
        self,
        matrix_df: pd.DataFrame,
        output_file: Optional[str] = None
    ):
        """Plot enzyme type distribution"""
        plt.figure(figsize=(12, 6))

        enzyme_counts = matrix_df["Enzyme"].value_counts()

        plt.bar(
            range(len(enzyme_counts)),
            enzyme_counts.values,
            color=self.colors["primary"]
        )
        plt.xticks(range(len(enzyme_counts)), enzyme_counts.index, rotation=45, ha='right')
        plt.xlabel("Enzyme Type")
        plt.ylabel("Count")
        plt.title("Enzyme Type Distribution")
        plt.tight_layout()

        if output_file is None:
            output_file = self.output_dir / "enzyme_distribution.png"

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved enzyme distribution plot to {output_file}")

    def plot_organism_distribution(
        self,
        matrix_df: pd.DataFrame,
        output_file: Optional[str] = None
    ):
        """Plot organism distribution pie chart"""
        plt.figure(figsize=(10, 8))

        organism_counts = matrix_df["Organism"].value_counts()

        colors_list = [
            self.colors["primary"],
            self.colors["secondary"],
            self.colors["accent"],
            "#6B9E78",
            "#D4AE6A"
        ]

        plt.pie(
            organism_counts.values,
            labels=organism_counts.index,
            autopct='%1.1f%%',
            colors=colors_list[:len(organism_counts)],
            startangle=90
        )
        plt.title("Organism Distribution")
        plt.axis('equal')

        if output_file is None:
            output_file = self.output_dir / "organism_distribution.png"

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved organism distribution plot to {output_file}")

    def plot_confidence_histogram(
        self,
        matrix_df: pd.DataFrame,
        output_file: Optional[str] = None
    ):
        """Plot confidence score distribution"""
        plt.figure(figsize=(10, 6))

        plt.hist(
            matrix_df["Confidence"],
            bins=20,
            color=self.colors["primary"],
            edgecolor='white',
            alpha=0.7
        )
        plt.xlabel("Confidence Score")
        plt.ylabel("Frequency")
        plt.title("Confidence Score Distribution")
        plt.axvline(
            matrix_df["Confidence"].mean(),
            color='red',
            linestyle='--',
            label=f'Mean: {matrix_df["Confidence"].mean():.2f}'
        )
        plt.legend()
        plt.tight_layout()

        if output_file is None:
            output_file = self.output_dir / "confidence_histogram.png"

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved confidence histogram to {output_file}")

    def plot_gh_family_distribution(
        self,
        matrix_df: pd.DataFrame,
        output_file: Optional[str] = None
    ):
        """Plot GH/AA family distribution"""
        plt.figure(figsize=(12, 6))

        gh_data = matrix_df[matrix_df["GH/AA Family"] != ""]
        if len(gh_data) == 0:
            logger.warning("No GH/AA family data to plot")
            return

        gh_counts = gh_data["GH/AA Family"].value_counts()

        plt.barh(
            range(len(gh_counts)),
            gh_counts.values,
            color=self.colors["secondary"]
        )
        plt.yticks(range(len(gh_counts)), gh_counts.index)
        plt.xlabel("Count")
        plt.ylabel("GH/AA Family")
        plt.title("Glycoside Hydrolase / Auxiliary Activity Family Distribution")
        plt.tight_layout()

        if output_file is None:
            output_file = self.output_dir / "gh_family_distribution.png"

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved GH family distribution plot to {output_file}")

    def plot_tissue_stage_heatmap(
        self,
        matrix_df: pd.DataFrame,
        output_file: Optional[str] = None
    ):
        """Plot heatmap of tissue x developmental stage"""
        plt.figure(figsize=(10, 8))

        # Create pivot table
        pivot = pd.crosstab(matrix_df["Tissue"], matrix_df["Stage"])

        plt.imshow(pivot.values, cmap='YlGn', aspect='auto')
        plt.colorbar(label='Count')

        plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha='right')
        plt.yticks(range(len(pivot.index)), pivot.index)

        plt.xlabel("Developmental Stage")
        plt.ylabel("Tissue")
        plt.title("Tissue × Developmental Stage Distribution")

        # Add value annotations
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                plt.text(j, i, str(pivot.values[i, j]),
                        ha='center', va='center', color='black')

        plt.tight_layout()

        if output_file is None:
            output_file = self.output_dir / "tissue_stage_heatmap.png"

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved tissue-stage heatmap to {output_file}")

    def create_summary_dashboard(self, matrix_df: pd.DataFrame):
        """Create comprehensive summary dashboard"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("EAB Enzyme Discovery Dashboard", fontsize=16, fontweight='bold')

        # 1. Enzyme distribution
        ax1 = axes[0, 0]
        enzyme_counts = matrix_df["Enzyme"].value_counts()
        ax1.bar(range(len(enzyme_counts)), enzyme_counts.values, color=self.colors["primary"])
        ax1.set_xticks(range(len(enzyme_counts)))
        ax1.set_xticklabels(enzyme_counts.index, rotation=45, ha='right')
        ax1.set_title("Enzyme Type Distribution")
        ax1.set_ylabel("Count")

        # 2. Confidence histogram
        ax2 = axes[0, 1]
        ax2.hist(matrix_df["Confidence"], bins=15, color=self.colors["primary"], alpha=0.7, edgecolor='white')
        ax2.axvline(matrix_df["Confidence"].mean(), color='red', linestyle='--',
                   label=f'Mean: {matrix_df["Confidence"].mean():.2f}')
        ax2.set_title("Confidence Distribution")
        ax2.set_xlabel("Confidence Score")
        ax2.set_ylabel("Frequency")
        ax2.legend()

        # 3. Organism distribution
        ax3 = axes[1, 0]
        organism_counts = matrix_df["Organism"].value_counts()
        ax3.pie(organism_counts.values, labels=organism_counts.index, autopct='%1.1f%%',
               startangle=90)
        ax3.set_title("Organism Distribution")

        # 4. Tissue distribution
        ax4 = axes[1, 1]
        tissue_counts = matrix_df["Tissue"].value_counts()
        ax4.barh(range(len(tissue_counts)), tissue_counts.values, color=self.colors["secondary"])
        ax4.set_yticks(range(len(tissue_counts)))
        ax4.set_yticklabels(tissue_counts.index)
        ax4.set_title("Tissue Distribution")
        ax4.set_xlabel("Count")

        plt.tight_layout()

        output_file = self.output_dir / "summary_dashboard.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved summary dashboard to {output_file}")

    def generate_all_plots(self, matrix_df: pd.DataFrame):
        """Generate all visualization plots"""
        logger.info("Generating all visualizations...")

        self.plot_enzyme_distribution(matrix_df)
        self.plot_organism_distribution(matrix_df)
        self.plot_confidence_histogram(matrix_df)
        self.plot_gh_family_distribution(matrix_df)
        self.plot_tissue_stage_heatmap(matrix_df)
        self.create_summary_dashboard(matrix_df)

        logger.info(f"All visualizations saved to {self.output_dir}")


def create_visualizer(output_dir: str = RESULTS_DIR) -> EnzymeVisualizer:
    """Factory function to create EnzymeVisualizer instance"""
    return EnzymeVisualizer(output_dir=output_dir)


if __name__ == "__main__":
    # Test visualizer with sample data
    import pandas as pd

    sample_data = {
        "Enzyme": ["cellulase", "laccase", "cellulase", "peroxidase", "xylanase"],
        "Organism": ["A. planipennis", "A. planipennis", "A. anxius", "A. planipennis", "C. femorata"],
        "Tissue": ["midgut", "gut", "midgut", "hindgut", "midgut"],
        "Stage": ["larval", "adult", "larval", "larval", "adult"],
        "Confidence": [0.92, 0.85, 0.88, 0.79, 0.91],
        "GH/AA Family": ["GH5", "", "GH9", "AA2", "GH10"]
    }

    df = pd.DataFrame(sample_data)

    visualizer = create_visualizer()
    visualizer.generate_all_plots(df)

    print(f"Visualizations saved to {visualizer.output_dir}")
