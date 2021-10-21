# Capstone


## TO DO

* __Implement geographic similarity thing__
  * sample function header:
    * ```
      # ID = the id of county of block
      # type = {'county' or 'block'}
      # colName = {'%hispanic' or ...}
      get_avg(int ID, str type, str colName){
	      // compute average of target variable for specified region
	      return theAverage
      }
      ```
  * some ideas:
    * just group by block
    * just group by county
    * group by county but assign a higher weight to regions in the same block
    * group by X but assign a higher weight to regions in the same block/County that have similar diverity scores
      * note that the diversity score has not yet been created
* __Diversity score__
  * given a list of variables that indicate diversity and the id of the region we are trying to quantify how diverse it is...
    * compute national average for the given variables
      * note that doing this read/computation every single time will take awhile, consider computing the averages and storing them in a file or dictionary
    * compute Eucledian distance between target region and national average
    * This value will probably still need to be normalized at the end
* __Misc__
  * implement include_strings in load_data()
  * Add y intercept to model
  * normalize all of the values
    * NOTE the percentage columns are normalized on the range [0, 100]. Need to be consistent
