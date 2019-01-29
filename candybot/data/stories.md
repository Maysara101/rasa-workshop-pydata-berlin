## not_buy
* greet
  - utter_greet
* first_query
  - utter_show_colors
* deny
  - utter_noworries

## list candy and bye
* greet
  - utter_greet
* color_query
  - utter_show_colors
* detail_query
  - utter_show_prices
* deny
  - utter_noworries

## Generated Story 2476928141338771446
* greet
  - utter_greet
* color_query
  - utter_show_colors
* deny
  - utter_noworries

## Customer list colors from database not hardcode
* db_list
  - action_list_colors
  - slot{"COLOR_LIST": "three colors"}
  - utter_list_colors