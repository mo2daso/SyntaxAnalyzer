import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from parser.parser import Node  # Fixed import path


class ParseTreeVisualizer:
    """Visualizes the parse tree using networkx and matplotlib"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_labels = {}
        self.node_colors = {}
        self.node_counter = 0

    def _get_node_id(self):
        """Generate a unique node identifier"""
        self.node_counter += 1
        return f"node_{self.node_counter}"

    def build_tree(self, node: Node, parent_id=None):
        """Build the networkx graph from the parse tree"""
        if not node:
            return
            
        current_id = self._get_node_id()
        
        # Set node properties
        self.node_labels[current_id] = f"{node.type}\n{node.value}"
        self.node_colors[current_id] = self._get_node_color(node.type)
        
        self.graph.add_node(current_id)
        if parent_id:
            self.graph.add_edge(parent_id, current_id)
            
        for child in node.children:
            self.build_tree(child, current_id)

    def _get_node_color(self, node_type: str) -> str:
        """Get the color for a node based on its type"""
        colors = {
            'operator': '#3498db',  # Blue
            'assign': '#e74c3c',    # Red
            'logical': '#2ecc71',   # Green
            'compare': '#f1c40f',   # Yellow
            'literal': '#9b59b6',   # Purple
            'group': '#95a5a6',     # Gray
        }
        return colors.get(node_type.lower(), '#34495e')  # Default dark blue

    def visualize(self, root_node: Node):
        """Create and return a matplotlib figure of the parse tree"""
        if not root_node:
            return None
            
        # Reset the graph state
        self.graph.clear()
        self.node_labels.clear()
        self.node_colors.clear()
        self.node_counter = 0
        
        # Build and draw the tree
        self.build_tree(root_node)
        
        plt.figure(figsize=(12, 8))
        pos = graphviz_layout(self.graph, prog="dot")
        
        nx.draw(self.graph, pos,
               labels=self.node_labels,
               node_color=[self.node_colors[node] for node in self.graph.nodes()],
               node_size=2500,
               font_size=10,
               font_weight='bold',
               font_color='white',
               edge_color='#95a5a6',
               width=2,
               arrows=True,
               arrowsize=20)
        
        plt.title("Parse Tree Visualization", pad=20, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return plt.gcf()