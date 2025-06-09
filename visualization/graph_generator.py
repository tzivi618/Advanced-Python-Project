import matplotlib.pyplot as plt
import io
from .graph_types import GraphType

class GraphGenerator:
    def __init__(self, analysis_results):
        self.results = analysis_results

    def generate(self, graph_type: GraphType):
        if graph_type == GraphType.HISTOGRAM:
            return self.generate_histogram()
        elif graph_type == GraphType.PIE:
            return self.generate_pie_chart()
        elif graph_type == GraphType.BAR:
            return self.generate_bar_chart()
        elif graph_type == GraphType.LINE:
            return self.generate_line_graph()
        else:
            raise ValueError("Unsupported graph type")

    def generate_histogram(self):
        func_lengths = self.results.get("function_lengths", [])
        plt.figure()
        plt.hist(func_lengths, bins=range(0, max(func_lengths + [1]) + 5, 5), color='skyblue', edgecolor='black')
        plt.title("Distribution of Function Lengths")
        plt.xlabel("Function Length (lines)")
        plt.ylabel("Number of Functions")
        return self.save_plot_to_bytes()

    def generate_pie_chart(self):
        issues_per_type = self.results.get("issues_per_type", {})
        labels = list(issues_per_type.keys())
        sizes = list(issues_per_type.values())
        plt.figure()
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Issues by Type")
        return self.save_plot_to_bytes()

    def generate_bar_chart(self):
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
        return self.save_plot_to_bytes()

    def generate_line_graph(self):
        issues_over_time = self.results.get("issues_over_time", [])
        plt.figure()
        plt.plot(range(len(issues_over_time)), issues_over_time, marker='o')
        plt.title("Issues Over Time")
        plt.xlabel("Push Index")
        plt.ylabel("Number of Issues")
        return self.save_plot_to_bytes()

    @staticmethod
    def save_plot_to_bytes():
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()