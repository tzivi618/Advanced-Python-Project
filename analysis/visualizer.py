import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generate_graphs(issues):
    function_lengths = [issue.length for issue in issues if hasattr(issue, "length") and issue.length is not None]
    plt.hist(function_lengths, bins=10)
    plt.title("Function Length Distribution")
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.savefig("function_length_distribution.png")
    plt.close()

    # הוספת גרפים נוספים לפי הצורך

    return ["function_length_distribution.png"]
