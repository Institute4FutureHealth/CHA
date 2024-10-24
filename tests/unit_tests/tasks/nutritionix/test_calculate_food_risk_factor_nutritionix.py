import pytest
from tasks.nutritionix import (
    CalculateFoodRiskFactor,
)


def test_query_nutritionix_execute():
    query = {
        "foods": [
            {
                "food_name": "cheeseburger",
                "brand_name": "null",
                "serving_qty": 1,
                "serving_unit": "item",
                "serving_weight_grams": 199,
                "nf_calories": 535.31,
                "nf_total_fat": 28.66,
                "nf_saturated_fat": 14,
                "nf_cholesterol": 95.52,
                "nf_sodium": 1176.09,
                "nf_total_carbohydrate": 39.24,
                "nf_dietary_fiber": 2.39,
                "nf_sugars": 7.16,
                "nf_protein": 30.27,
                "nf_potassium": 443.77,
                "nf_p": 364.17,
                "full_nutrients": [
                    {"attr_id": 203, "value": 30.2679},
                    {"attr_id": 204, "value": 28.656},
                    {"attr_id": 205, "value": 39.2428},
                    {"attr_id": 207, "value": 4.5969},
                    {"attr_id": 208, "value": 535.31},
                    {"attr_id": 209, "value": 25.87},
                    {"attr_id": 210, "value": 0.2985},
                    {"attr_id": 211, "value": 1.8507},
                    {"attr_id": 212, "value": 2.5671},
                    {"attr_id": 213, "value": 0.9353},
                    {"attr_id": 214, "value": 1.5124},
                    {"attr_id": 221, "value": 0},
                    {"attr_id": 255, "value": 96.2364},
                    {"attr_id": 262, "value": 0},
                    {"attr_id": 263, "value": 0},
                    {"attr_id": 268, "value": 2242.73},
                    {"attr_id": 269, "value": 7.164},
                    {"attr_id": 291, "value": 2.388},
                    {"attr_id": 301, "value": 356.21},
                    {"attr_id": 303, "value": 2.0298},
                    {"attr_id": 304, "value": 51.74},
                    {"attr_id": 305, "value": 364.17},
                    {"attr_id": 306, "value": 443.77},
                    {"attr_id": 307, "value": 1176.09},
                    {"attr_id": 309, "value": 5.6317},
                    {"attr_id": 312, "value": 0.1493},
                    {"attr_id": 315, "value": 0.3244},
                    {"attr_id": 317, "value": 49.153},
                    {"attr_id": 318, "value": 471.63},
                    {"attr_id": 319, "value": 93.53},
                    {"attr_id": 320, "value": 101.49},
                    {"attr_id": 321, "value": 93.53},
                    {"attr_id": 322, "value": 1.99},
                    {"attr_id": 323, "value": 0.398},
                    {"attr_id": 324, "value": 5.97},
                    {"attr_id": 328, "value": 0.199},
                    {"attr_id": 334, "value": 3.98},
                    {"attr_id": 337, "value": 1611.9},
                    {"attr_id": 338, "value": 33.83},
                    {"attr_id": 341, "value": 5.4924},
                    {"attr_id": 342, "value": 0.6368},
                    {"attr_id": 343, "value": 0.1194},
                    {"attr_id": 345, "value": 0},
                    {"attr_id": 346, "value": 0},
                    {"attr_id": 347, "value": 0},
                    {"attr_id": 401, "value": 0.597},
                    {"attr_id": 404, "value": 0.2368},
                    {"attr_id": 405, "value": 0.5174},
                    {"attr_id": 406, "value": 8.0595},
                    {"attr_id": 410, "value": 1.1741},
                    {"attr_id": 415, "value": 0.1851},
                    {"attr_id": 417, "value": 31.84},
                    {"attr_id": 418, "value": 3.4825},
                    {"attr_id": 421, "value": 75.023},
                    {"attr_id": 429, "value": 0},
                    {"attr_id": 430, "value": 8.756},
                    {"attr_id": 431, "value": 23.88},
                    {"attr_id": 432, "value": 7.96},
                    {"attr_id": 435, "value": 47.76},
                    {"attr_id": 601, "value": 95.52},
                    {"attr_id": 606, "value": 13.9957},
                    {"attr_id": 607, "value": 0.3861},
                    {"attr_id": 608, "value": 0.1313},
                    {"attr_id": 609, "value": 0.0975},
                    {"attr_id": 610, "value": 0.2149},
                    {"attr_id": 611, "value": 0.2527},
                    {"attr_id": 612, "value": 1.4428},
                    {"attr_id": 613, "value": 7.2177},
                    {"attr_id": 614, "value": 3.7651},
                    {"attr_id": 615, "value": 0.0398},
                    {"attr_id": 617, "value": 10.6306},
                    {"attr_id": 618, "value": 2.0079},
                    {"attr_id": 619, "value": 0.2527},
                    {"attr_id": 620, "value": 0.0577},
                    {"attr_id": 621, "value": 0},
                    {"attr_id": 624, "value": 0},
                    {"attr_id": 625, "value": 0.2149},
                    {"attr_id": 626, "value": 0.9174},
                    {"attr_id": 627, "value": 0.1552},
                    {"attr_id": 628, "value": 0.0975},
                    {"attr_id": 629, "value": 0},
                    {"attr_id": 630, "value": 0},
                    {"attr_id": 631, "value": 0},
                    {"attr_id": 645, "value": 11.8584},
                    {"attr_id": 646, "value": 2.5154},
                    {"attr_id": 652, "value": 0.1751},
                    {"attr_id": 653, "value": 0.2726},
                    {"attr_id": 654, "value": 0},
                    {"attr_id": 672, "value": 0},
                    {"attr_id": 687, "value": 0},
                    {"attr_id": 689, "value": 0.0398},
                    {"attr_id": 697, "value": 0},
                ],
                "nix_brand_name": "null",
                "nix_brand_id": "null",
                "nix_item_name": "null",
                "nix_item_id": "null",
                "upc": "null",
                "consumed_at": "2024-01-28T13:00:00+00:00",
                "metadata": {"is_raw_food": False},
                "source": 1,
                "ndb_no": 21398,
                "tags": {
                    "item": "cheeseburger",
                    "measure": "null",
                    "quantity": "1.0",
                    "food_group": 8,
                    "tag_id": 445,
                },
                "alt_measures": [
                    {
                        "serving_weight": 199,
                        "measure": "item",
                        "seq": 1,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 100,
                        "measure": "g",
                        "seq": "null",
                        "qty": 100,
                    },
                    {
                        "serving_weight": 28.3495,
                        "measure": "wt. oz",
                        "seq": "null",
                        "qty": 1,
                    },
                ],
                "lat": "null",
                "lng": "null",
                "meal_type": 1,
                "photo": {
                    "thumb": "https://nix-tag-images.s3.amazonaws.com/445_thumb.jpg",
                    "highres": "https://nix-tag-images.s3.amazonaws.com/445_highres.jpg",
                    "is_user_uploaded": False,
                },
                "sub_recipe": "null",
                "class_code": "null",
                "brick_code": "null",
                "tag_id": "null",
            },
            {
                "food_name": "milk",
                "brand_name": "null",
                "serving_qty": 1,
                "serving_unit": "cup",
                "serving_weight_grams": 244,
                "nf_calories": 122,
                "nf_total_fat": 4.83,
                "nf_saturated_fat": 3.07,
                "nf_cholesterol": 19.52,
                "nf_sodium": 114.68,
                "nf_total_carbohydrate": 11.71,
                "nf_dietary_fiber": 0,
                "nf_sugars": 12.35,
                "nf_protein": 8.05,
                "nf_potassium": 341.6,
                "nf_p": 224.48,
                "full_nutrients": [
                    {"attr_id": 203, "value": 8.052},
                    {"attr_id": 204, "value": 4.8312},
                    {"attr_id": 205, "value": 11.712},
                    {"attr_id": 207, "value": 1.7324},
                    {"attr_id": 208, "value": 122},
                    {"attr_id": 210, "value": 0.0244},
                    {"attr_id": 211, "value": 0.0244},
                    {"attr_id": 212, "value": 0.0244},
                    {"attr_id": 213, "value": 12.2244},
                    {"attr_id": 214, "value": 0.0244},
                    {"attr_id": 221, "value": 0},
                    {"attr_id": 255, "value": 217.6724},
                    {"attr_id": 262, "value": 0},
                    {"attr_id": 263, "value": 0},
                    {"attr_id": 268, "value": 512.4},
                    {"attr_id": 269, "value": 12.3464},
                    {"attr_id": 287, "value": 0.0488},
                    {"attr_id": 291, "value": 0},
                    {"attr_id": 301, "value": 292.8},
                    {"attr_id": 303, "value": 0.0488},
                    {"attr_id": 304, "value": 26.84},
                    {"attr_id": 305, "value": 224.48},
                    {"attr_id": 306, "value": 341.6},
                    {"attr_id": 307, "value": 114.68},
                    {"attr_id": 309, "value": 1.1712},
                    {"attr_id": 312, "value": 0.0146},
                    {"attr_id": 313, "value": 8.296},
                    {"attr_id": 315, "value": 0.0342},
                    {"attr_id": 317, "value": 6.1},
                    {"attr_id": 318, "value": 463.6},
                    {"attr_id": 319, "value": 134.2},
                    {"attr_id": 320, "value": 134.2},
                    {"attr_id": 321, "value": 9.76},
                    {"attr_id": 322, "value": 0},
                    {"attr_id": 323, "value": 0.0732},
                    {"attr_id": 324, "value": 119.56},
                    {"attr_id": 326, "value": 2.928},
                    {"attr_id": 328, "value": 2.928},
                    {"attr_id": 334, "value": 0},
                    {"attr_id": 337, "value": 0},
                    {"attr_id": 338, "value": 0},
                    {"attr_id": 341, "value": 0},
                    {"attr_id": 342, "value": 0},
                    {"attr_id": 343, "value": 0},
                    {"attr_id": 344, "value": 0},
                    {"attr_id": 345, "value": 0},
                    {"attr_id": 346, "value": 0},
                    {"attr_id": 347, "value": 0},
                    {"attr_id": 401, "value": 0.488},
                    {"attr_id": 404, "value": 0.0952},
                    {"attr_id": 405, "value": 0.4514},
                    {"attr_id": 406, "value": 0.2245},
                    {"attr_id": 410, "value": 0.8686},
                    {"attr_id": 415, "value": 0.0927},
                    {"attr_id": 417, "value": 12.2},
                    {"attr_id": 418, "value": 1.2932},
                    {"attr_id": 421, "value": 40.016},
                    {"attr_id": 429, "value": 0},
                    {"attr_id": 430, "value": 0.488},
                    {"attr_id": 431, "value": 0},
                    {"attr_id": 432, "value": 12.2},
                    {"attr_id": 435, "value": 12.2},
                    {"attr_id": 454, "value": 2.196},
                    {"attr_id": 501, "value": 0.1025},
                    {"attr_id": 502, "value": 0.344},
                    {"attr_id": 503, "value": 0.4172},
                    {"attr_id": 504, "value": 0.7637},
                    {"attr_id": 505, "value": 0.6734},
                    {"attr_id": 506, "value": 0.2123},
                    {"attr_id": 507, "value": 0.0488},
                    {"attr_id": 508, "value": 0.4172},
                    {"attr_id": 509, "value": 0.4075},
                    {"attr_id": 510, "value": 0.527},
                    {"attr_id": 511, "value": 0.2294},
                    {"attr_id": 512, "value": 0.244},
                    {"attr_id": 513, "value": 0.2733},
                    {"attr_id": 514, "value": 0.6905},
                    {"attr_id": 515, "value": 1.8105},
                    {"attr_id": 516, "value": 0.1586},
                    {"attr_id": 517, "value": 0.7954},
                    {"attr_id": 518, "value": 0.4856},
                    {"attr_id": 521, "value": 0},
                    {"attr_id": 601, "value": 19.52},
                    {"attr_id": 605, "value": 0.2074},
                    {"attr_id": 606, "value": 3.0671},
                    {"attr_id": 607, "value": 0.1879},
                    {"attr_id": 608, "value": 0.0976},
                    {"attr_id": 609, "value": 0.0488},
                    {"attr_id": 610, "value": 0.1196},
                    {"attr_id": 611, "value": 0.1342},
                    {"attr_id": 612, "value": 0.427},
                    {"attr_id": 613, "value": 1.3615},
                    {"attr_id": 614, "value": 0.5929},
                    {"attr_id": 615, "value": 0.0098},
                    {"attr_id": 617, "value": 1.2395},
                    {"attr_id": 618, "value": 0.1513},
                    {"attr_id": 619, "value": 0.0195},
                    {"attr_id": 620, "value": 0},
                    {"attr_id": 621, "value": 0},
                    {"attr_id": 624, "value": 0.0049},
                    {"attr_id": 625, "value": 0.0366},
                    {"attr_id": 626, "value": 0.0659},
                    {"attr_id": 627, "value": 0},
                    {"attr_id": 628, "value": 0.0049},
                    {"attr_id": 629, "value": 0},
                    {"attr_id": 630, "value": 0},
                    {"attr_id": 631, "value": 0},
                    {"attr_id": 638, "value": 0},
                    {"attr_id": 639, "value": 0},
                    {"attr_id": 641, "value": 0},
                    {"attr_id": 645, "value": 1.3664},
                    {"attr_id": 646, "value": 0.1781},
                    {"attr_id": 652, "value": 0.0488},
                    {"attr_id": 653, "value": 0.0268},
                    {"attr_id": 663, "value": 0.1903},
                    {"attr_id": 673, "value": 0.0659},
                    {"attr_id": 674, "value": 1.0492},
                    {"attr_id": 675, "value": 0.1342},
                    {"attr_id": 687, "value": 0.0122},
                    {"attr_id": 689, "value": 0.0073},
                    {"attr_id": 693, "value": 0.1903},
                    {"attr_id": 695, "value": 0.0171},
                    {"attr_id": 696, "value": 0.0049},
                    {"attr_id": 697, "value": 0.0098},
                    {"attr_id": 851, "value": 0.0195},
                ],
                "nix_brand_name": "null",
                "nix_brand_id": "null",
                "nix_item_name": "null",
                "nix_item_id": "null",
                "upc": "null",
                "consumed_at": "2024-01-28T13:00:00+00:00",
                "metadata": {"is_raw_food": False},
                "source": 1,
                "ndb_no": 1079,
                "tags": {
                    "item": "2% milk",
                    "measure": "null",
                    "quantity": "1.0",
                    "food_group": 1,
                    "tag_id": 377,
                },
                "alt_measures": [
                    {
                        "serving_weight": 244,
                        "measure": "cup",
                        "seq": 1,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 30.5,
                        "measure": "fl oz",
                        "seq": 2,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 976,
                        "measure": "quart",
                        "seq": 3,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 100,
                        "measure": "g",
                        "seq": "null",
                        "qty": 100,
                    },
                    {
                        "serving_weight": 5.08,
                        "measure": "tsp",
                        "seq": 101,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 15.25,
                        "measure": "tbsp",
                        "seq": 102,
                        "qty": 1,
                    },
                ],
                "lat": "null",
                "lng": "null",
                "meal_type": 1,
                "photo": {
                    "thumb": "https://nix-tag-images.s3.amazonaws.com/377_thumb.jpg",
                    "highres": "https://nix-tag-images.s3.amazonaws.com/377_highres.jpg",
                    "is_user_uploaded": False,
                },
                "sub_recipe": "null",
                "class_code": "null",
                "brick_code": "null",
                "tag_id": "null",
            },
            {
                "food_name": "eggs",
                "brand_name": "null",
                "serving_qty": 2,
                "serving_unit": "large",
                "serving_weight_grams": 100,
                "nf_calories": 143,
                "nf_total_fat": 9.51,
                "nf_saturated_fat": 3.13,
                "nf_cholesterol": 372,
                "nf_sodium": 142,
                "nf_total_carbohydrate": 0.72,
                "nf_dietary_fiber": 0,
                "nf_sugars": 0.37,
                "nf_protein": 12.56,
                "nf_potassium": 138,
                "nf_p": 198,
                "full_nutrients": [
                    {"attr_id": 203, "value": 12.56},
                    {"attr_id": 204, "value": 9.51},
                    {"attr_id": 205, "value": 0.72},
                    {"attr_id": 207, "value": 1.06},
                    {"attr_id": 208, "value": 143},
                    {"attr_id": 210, "value": 0},
                    {"attr_id": 211, "value": 0.37},
                    {"attr_id": 212, "value": 0},
                    {"attr_id": 213, "value": 0},
                    {"attr_id": 214, "value": 0},
                    {"attr_id": 221, "value": 0},
                    {"attr_id": 255, "value": 76.15},
                    {"attr_id": 262, "value": 0},
                    {"attr_id": 263, "value": 0},
                    {"attr_id": 268, "value": 599},
                    {"attr_id": 269, "value": 0.37},
                    {"attr_id": 287, "value": 0},
                    {"attr_id": 291, "value": 0},
                    {"attr_id": 301, "value": 56},
                    {"attr_id": 303, "value": 1.75},
                    {"attr_id": 304, "value": 12},
                    {"attr_id": 305, "value": 198},
                    {"attr_id": 306, "value": 138},
                    {"attr_id": 307, "value": 142},
                    {"attr_id": 309, "value": 1.29},
                    {"attr_id": 312, "value": 0.072},
                    {"attr_id": 313, "value": 1.1},
                    {"attr_id": 315, "value": 0.028},
                    {"attr_id": 317, "value": 30.7},
                    {"attr_id": 318, "value": 540},
                    {"attr_id": 319, "value": 160},
                    {"attr_id": 320, "value": 160},
                    {"attr_id": 321, "value": 0},
                    {"attr_id": 322, "value": 0},
                    {"attr_id": 323, "value": 1.05},
                    {"attr_id": 324, "value": 82},
                    {"attr_id": 326, "value": 2},
                    {"attr_id": 328, "value": 2},
                    {"attr_id": 334, "value": 9},
                    {"attr_id": 337, "value": 0},
                    {"attr_id": 338, "value": 503},
                    {"attr_id": 341, "value": 0.01},
                    {"attr_id": 342, "value": 0.5},
                    {"attr_id": 343, "value": 0.06},
                    {"attr_id": 344, "value": 0.06},
                    {"attr_id": 345, "value": 0},
                    {"attr_id": 346, "value": 0.01},
                    {"attr_id": 347, "value": 0},
                    {"attr_id": 401, "value": 0},
                    {"attr_id": 404, "value": 0.04},
                    {"attr_id": 405, "value": 0.457},
                    {"attr_id": 406, "value": 0.075},
                    {"attr_id": 410, "value": 1.533},
                    {"attr_id": 415, "value": 0.17},
                    {"attr_id": 417, "value": 47},
                    {"attr_id": 418, "value": 0.89},
                    {"attr_id": 421, "value": 293.8},
                    {"attr_id": 429, "value": 0.1},
                    {"attr_id": 430, "value": 0.3},
                    {"attr_id": 431, "value": 0},
                    {"attr_id": 432, "value": 47},
                    {"attr_id": 435, "value": 47},
                    {"attr_id": 454, "value": 0.3},
                    {"attr_id": 501, "value": 0.167},
                    {"attr_id": 502, "value": 0.556},
                    {"attr_id": 503, "value": 0.671},
                    {"attr_id": 504, "value": 1.086},
                    {"attr_id": 505, "value": 0.912},
                    {"attr_id": 506, "value": 0.38},
                    {"attr_id": 507, "value": 0.272},
                    {"attr_id": 508, "value": 0.68},
                    {"attr_id": 509, "value": 0.499},
                    {"attr_id": 510, "value": 0.858},
                    {"attr_id": 511, "value": 0.82},
                    {"attr_id": 512, "value": 0.309},
                    {"attr_id": 513, "value": 0.735},
                    {"attr_id": 514, "value": 1.329},
                    {"attr_id": 515, "value": 1.673},
                    {"attr_id": 516, "value": 0.432},
                    {"attr_id": 517, "value": 0.512},
                    {"attr_id": 518, "value": 0.971},
                    {"attr_id": 601, "value": 372},
                    {"attr_id": 605, "value": 0.038},
                    {"attr_id": 606, "value": 3.126},
                    {"attr_id": 607, "value": 0.004},
                    {"attr_id": 608, "value": 0},
                    {"attr_id": 609, "value": 0.004},
                    {"attr_id": 610, "value": 0.006},
                    {"attr_id": 611, "value": 0},
                    {"attr_id": 612, "value": 0.033},
                    {"attr_id": 613, "value": 2.231},
                    {"attr_id": 614, "value": 0.811},
                    {"attr_id": 615, "value": 0.003},
                    {"attr_id": 617, "value": 3.411},
                    {"attr_id": 618, "value": 1.555},
                    {"attr_id": 619, "value": 0.048},
                    {"attr_id": 620, "value": 0.188},
                    {"attr_id": 621, "value": 0.058},
                    {"attr_id": 624, "value": 0.004},
                    {"attr_id": 625, "value": 0.007},
                    {"attr_id": 626, "value": 0.201},
                    {"attr_id": 627, "value": 0},
                    {"attr_id": 628, "value": 0.027},
                    {"attr_id": 629, "value": 0},
                    {"attr_id": 630, "value": 0},
                    {"attr_id": 631, "value": 0.007},
                    {"attr_id": 645, "value": 3.658},
                    {"attr_id": 646, "value": 1.911},
                    {"attr_id": 652, "value": 0.008},
                    {"attr_id": 653, "value": 0.022},
                    {"attr_id": 654, "value": 0},
                    {"attr_id": 662, "value": 0.003},
                    {"attr_id": 663, "value": 0.023},
                    {"attr_id": 664, "value": 0},
                    {"attr_id": 670, "value": 0.012},
                    {"attr_id": 671, "value": 0},
                    {"attr_id": 672, "value": 0.018},
                    {"attr_id": 673, "value": 0.198},
                    {"attr_id": 674, "value": 3.388},
                    {"attr_id": 675, "value": 1.531},
                    {"attr_id": 676, "value": 0},
                    {"attr_id": 685, "value": 0.012},
                    {"attr_id": 687, "value": 0.012},
                    {"attr_id": 689, "value": 0.023},
                    {"attr_id": 693, "value": 0.026},
                    {"attr_id": 695, "value": 0.012},
                    {"attr_id": 697, "value": 0},
                    {"attr_id": 851, "value": 0.036},
                    {"attr_id": 852, "value": 0.001},
                    {"attr_id": 853, "value": 0.022},
                    {"attr_id": 858, "value": 0.013},
                ],
                "nix_brand_name": "null",
                "nix_brand_id": "null",
                "nix_item_name": "null",
                "nix_item_id": "null",
                "upc": "null",
                "consumed_at": "2024-01-28T13:00:00+00:00",
                "metadata": {"is_raw_food": False},
                "source": 1,
                "ndb_no": 1123,
                "tags": {
                    "item": "eggs",
                    "measure": "null",
                    "quantity": "2",
                    "food_group": 2,
                    "tag_id": 542,
                },
                "alt_measures": [
                    {
                        "serving_weight": 50,
                        "measure": "large",
                        "seq": 1,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 56,
                        "measure": "extra large",
                        "seq": 2,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 63,
                        "measure": "jumbo",
                        "seq": 3,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 243,
                        "measure": "cup (4.86 large eggs)",
                        "seq": 5,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 44,
                        "measure": "medium",
                        "seq": 6,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 38,
                        "measure": "small",
                        "seq": 7,
                        "qty": 1,
                    },
                    {
                        "serving_weight": 100,
                        "measure": "g",
                        "seq": "null",
                        "qty": 100,
                    },
                    {
                        "serving_weight": 28.3495,
                        "measure": "wt. oz",
                        "seq": "null",
                        "qty": 1,
                    },
                ],
                "lat": "null",
                "lng": "null",
                "meal_type": 1,
                "photo": {
                    "thumb": "https://nix-tag-images.s3.amazonaws.com/542_thumb.jpg",
                    "highres": "https://nix-tag-images.s3.amazonaws.com/542_highres.jpg",
                    "is_user_uploaded": False,
                },
                "sub_recipe": "null",
                "class_code": "null",
                "brick_code": "null",
                "tag_id": "null",
            },
        ]
    }

    calculate_food_risk_factor_task = CalculateFoodRiskFactor()

    result = calculate_food_risk_factor_task._execute(
        [{"data": query}]
    )
    print(result)
    assert isinstance(result, str)
