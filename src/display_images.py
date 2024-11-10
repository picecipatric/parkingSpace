import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImagePlotter: 
    def __init__(self):
        self.dictionary_images:dict[str, cv2.typing.MatLike] = {}
    
    def add_image_to_plot(self, name_image:str, image:cv2.typing.MatLike) -> bool:
        """add image to be plotted.

        Args:
            name_image (str): name of image
            image (cv2.typing.MatLike): image in opencv format

        Returns:
            bool: True, if successful. False, otherwise. 
        """
        if len(self.dictionary_images) > 0:
            if name_image in self.dictionary_images:
                print("ERROR: Image couldn't be added. Name already exists.")
                return False
        self.dictionary_images[name_image] = image
        return True
    
    
    def plot_images(self) -> None:
        """
        Plot/display images.
        """
        plt.close('all')
    
        amount_of_images = len(self.dictionary_images)
        names_images = list(self.dictionary_images)
        images = list(self.dictionary_images.values())
        
        print(names_images)
        
        subplot_rows, subplot_columns = self._get_subplot_layout(amount_of_images)
    
        figure, ax_array = plt.subplots(subplot_rows, subplot_columns, 
                                    squeeze=False, layout="constrained")
        for index in range(0, subplot_rows * subplot_columns): 
            id_y = index // subplot_columns
            id_x = index % subplot_columns
            
            if index < amount_of_images:
                img = cv2.cvtColor(images[index], cv2.COLOR_BGR2RGB)
                ax_array[id_y, id_x].imshow(img)
                
                subplot_title = f"{index+1}.) {names_images[index]}"
                ax_array[id_y, id_x].set_title(subplot_title)
            ax_array[id_y, id_x].axis('off')
        plt.show()
    
    
    def _get_subplot_layout(self, number_of_elements:int)->tuple[int, int]:
        """Get layout of subplot in regards to amount of elements

        Args:
            number_of_elements (int): Number of elements which will be in subplot

        Returns:
            tuple[int, int]: number of subplot rows and columns  
        """
        if number_of_elements <= 0:
            return (1, 1)
    
        subplot_columns = np.ceil(np.sqrt(number_of_elements))
        subplot_rows = np.ceil(number_of_elements/subplot_columns)
    
        subplot_columns = int(subplot_columns)
        subplot_rows = int(subplot_rows)
    
        return (subplot_rows, subplot_columns)
    

    

