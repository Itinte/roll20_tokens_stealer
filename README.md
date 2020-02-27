# [WIP] Roll20 Tokens Stealer 
Download any roll20 (top-down) tokens from the marketplace for free
The model is especially good at detouring D. North and D. Night drawing style.
Readme will be completed and code improved

/!\ config, requirements and tests still need to be implemented...

## 2 commands : 
- roll20 market place url scrapper:  
```
python scrap_url_cmd.py --url https://marketplace.roll20.net/browse/set/5248/boss-monster-token-set-14
```
- detour scrapped images with a pre-trained Unet
```
python detour_cmd.py --src 'SRC_PATH/scrapping_results/' --tgt 'TGT_PATH/roll20_detour/predictions/' --model 'MODEL_PATH/model/unet_2_06.h5'
```

/!\ Unet pre-trained weights and training data are not shared in this repository
