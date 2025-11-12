All files and created CSVs must be in the same folder.  
Can use scrapeAll.py on its own to create correlation data csvs, and can use those to create heatmaps if needed (try seaborn).  
Run dabbly.py on dabble.json, then scrapeAll.py, then suggest.py.  
Results can be interpreted as: (Player A -> Player B: Int) if Player A gets an assist, Player B will score a point on the same goal with probability (Int).  
