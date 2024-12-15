import matplotlib.pyplot as plt
import numpy as np

from src.parking_spot_parameters import ParkingSpot


plt.table

class DisplayOverviewer:
    def __init__(self, parking_spots:list[ParkingSpot]):
        self.matrix=[]
        self.parking_spots = parking_spots
        
    def create_table(self, )->list[list[str]]:
        amount_spots = len(self.parking_spots)
        amount_cols = int(np.abs(np.ceil(np.sqrt(amount_spots))))
        row = []
        for i, spot in enumerate(self.parking_spots):
            # text = "{:3d}: {:4.2f}".format(spot.lable_id,
            #                                spot.time.time_delta/60)
            text = "{:3d}".format(spot.lable_id)
            row.append(text)
            if i%amount_cols == amount_cols-1:
                self.matrix.append(row)
                row = []
            if i == amount_spots-1:
                if 0 < len(row) < amount_cols:
                    for i in range(i%amount_cols, amount_cols-1):
                        row.append("")
                    self.matrix.append(row)
        return None

    def show_overview(self):       
        # Create a figure
        fig, ax = plt.subplots()

        # Create a table-like heatmap using imshow (empty background)
        ax.imshow([[0] * len(row) for row in self.matrix], cmap="viridis", alpha=0)

        # Add annotations (text) to each cell
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                ax.text(j, i, f"{val}", ha="center", va="center", color="black")

        # Adjust axis and display
        ax.set_xticks(range(len(self.matrix[0])))
        ax.set_yticks(range(len(self.matrix)))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.show()
