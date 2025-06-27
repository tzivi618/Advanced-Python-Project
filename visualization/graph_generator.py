import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, os
from .graph_types import GraphType

class GraphGenerator:
    """
    Generates visual representations (graphs) of analysis results.
    """

    def __init__(self, analysis_results, output_dir='graphs'):
        """
        Initializes the graph generator with analysis results and output directory.
        """
        self.results = analysis_results
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.strategies = {
            GraphType.HISTOGRAM: self.generate_histogram,
            GraphType.PIE: self.generate_pie_chart,
            GraphType.BAR: self.generate_bar_chart,
            GraphType.LINE: self.generate_line_graph,
        }

    def generate(self, graph_type: GraphType):
        """
        Generates a graph based on the specified type.
        """
        strategy = self.strategies.get(graph_type)
        if strategy is None:
            raise ValueError("Unsupported graph type")
        return strategy()

    def generate_histogram(self):
        """
        Generates a histogram of function lengths.
        """
        func_lengths = self.results.get("function_lengths", [])
        plt.figure()
        plt.hist(func_lengths, bins=range(0, max(func_lengths + [1]) + 5, 5), color='skyblue', edgecolor='black')
        plt.title("Distribution of Function Lengths")
        plt.xlabel("Function Length (lines)")
        plt.ylabel("Number of Functions")
        return self.save_plot_to_bytes('histogram.png')

    def generate_pie_chart(self):
        """
        Generates a pie chart of issues by type.
        """
        issues_per_type = self.results.get("issues_per_type", {})
        labels = list(issues_per_type.keys())
        sizes = list(issues_per_type.values())
        plt.figure()
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Issues by Type")
        return self.save_plot_to_bytes('pie.png')

    def generate_bar_chart(self):
        """
        Generates a bar chart of issues per file.
        """
        issues_per_file = self.results.get("issues_per_file", {})
        files = list(issues_per_file.keys())
        counts = list(issues_per_file.values())
        plt.figure(figsize=(8, 4))
        plt.bar(files, counts, color='orange')
        plt.title("Number of Issues per File")
        plt.xlabel("File")
        plt.ylabel("Number of Issues")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return self.save_plot_to_bytes('bar.png')

    def generate_line_graph(self):
        """
        Generates a line graph of issues over time.
        """
        issues_over_time = self.results.get("issues_over_time", [])
        plt.figure()
        plt.plot(range(len(issues_over_time)), issues_over_time, marker='o')
        plt.title("Issues Over Time")
        plt.xlabel("Push Index")
        plt.ylabel("Number of Issues")
        return self.save_plot_to_bytes('line.png')

    def save_plot_to_bytes(self, filename):
        """
        Saves the current matplotlib figure to both a file and bytes object.
        """
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.savefig(os.path.join(self.output_dir, filename), format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()
