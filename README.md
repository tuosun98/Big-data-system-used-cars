# Big_data_system_used_cars
This is a Big data system used cars for saving, analyse and modeling
The data are from cars.com. The dataset contains the information of 30627 used cars on sale. All of the cars are within 20 miles from ZIP code 90013. There are three files in this dataset

# car_data.json

The following is the information of a car in `car_data.json`.

* `822058788`---------------------------------------------------------------ID code for the car

  * `vehicle_head_info`--------------------------------------------header of information

    * `title`: " 2003 BMW Z4 3.0i Roadster"-------------title of used car. 

      ​																		    	   This contains the year, the maker and the model.

    * `odometer`: "106,517 miles"-----------------------------odometer of the car.

    * `price`: "$8,995"---------------------------------------------price of the car

  * `seller_info`------------------------------------------------------seller information

    * `seller_name`: "Sold by Shane's..."-------------------name of seller
    * `seller_rateing`: "4.1"-----------------------------------rating of seller 4.1/5.0
    * `seller_reviews_count`: "33 Reviews"-------------the number of reviews
    * `seller_position`: "ShermanOaks,CA91423"---current position of the car
    * `seller_notes`: ”Welcome to SHANE CARS“------notes written by selle

  * `basics`--------------------------------------------------------------basic information

    * `Fuel Type`: "Gasoline"
    * `Exterior Color`: "Blue"
    * `City MPG`: "21"
    * `Interior Color`: "Black"
    * `Highway MPG`: "29"
    * `Stock`: "3996"-----------------------------------------------Stock number of the car
    * `Drivetrain`: "RWD"
    * `Transmission`: "6-Speed SMG II"
    * `Engine`: "3.0L I6 24V MPFI DOHC"
    * `VIN`: "4USBT53453LT24117"---------------------------Unique Vin code
    * `Mileage`: "106,517"

  * `all_features`:[----------------------------------------------------a list of features of the car

    ​	"ABS and Driveline Traction Control",

    ​	...		

    ]

# key_pos.csv

This is a csv file with a column of ID code and a column of position information

* `unname` ：This is the index of csv file from 0 to 30626
* `ID` : ID code
* `Position` : the city and ZIP code of the car.

###### Tips: By using zip code API, you can get the latitude and longitude of the car. This can be additional data for training

# key_vin.csv

This is a csv file with a column of ID code and a column of vin code for the car

* `unname` ：This is the index of csv file from 0 to 30626
* `ID` : ID code
* `VIN` :  VIN is unique for each vehicle.

##### Tips: By using NHTSA API, you can decode VIN for getting more information of the car. These information may be helpful for your training
