# dataMax
A repository based on extracting the Top Picks of Kaggles API for hboMAX

For a person to use this, they need to be sure they have a Kaggle Account, with a user name and a token in order to download the dataset of their choosing.

this is the first time I have used this library, but I have had an assignment to generate data and then modify the data in some way. So I effectively did so using a python script which is dedicated to the full HBO Max Dataset. BUT! I have included the simple download script that someone can use for any data set of their choosing. They could use that script and then build off of the download to accomplish whatever it is that might be needed.

The first step to working with this is using the script "download_and_analyze.py" || The other file "retrieve_data.py" is a clever way to setup a project for retrieving data given the use of the developer. It's just a starting point!

Running the file download_and_analyze.py will generate a text file which is needed for modifying the text for tokenization for future ML projects, or any type of data testing. For this project it's simply there to read and modify as part of the GUI which displays the data through matplot library creating a visual experience. All someone has to do after creating the file and downloading the dataset is run hbo_dataMax.py and there are four ways to visualize the top movie picks on HBO!

If anyone uses this, have fun, feel free to expand for your own learning and exploration!
