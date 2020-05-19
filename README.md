/*******************Pre-requisites to run CC-GA*******************************/ <br/>

1-install Python-3  <br/>
2-install pyparsing package  <br/>
3-install networkx  <br/>

/******************run the program using this command*************************/

run main.py -- i.e., python main.py

/* parameters setting and input networks can be provided in params.py file


/*****************The algorithm will produce three types of files*************/

1- "results.csv"  contains the parameter setting and resulted modularities
2- "network_name.gml" a gml files contains the community structure of the network
3 -"network_name.text" contains list of communities discoverd by CC-GA under gml directory

Please cite our paper if you are using this source code in your project.

@article{said2018cc,
  title={CC-GA: A clustering coefficient based genetic algorithm for detecting communities in social networks},
  author={Said, Anwar and Abbasi, Rabeeh Ayaz and Maqbool, Onaiza and Daud, Ali and Aljohani, Naif Radi},
  journal={Applied Soft Computing},
  volume={63},
  pages={59--70},
  year={2018},
  publisher={Elsevier}
}
