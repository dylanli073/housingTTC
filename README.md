# housingTTC
### Dylan Li, David Moon, Yi Lin Wang
Modifying the classically known TTC mechanism for housing allocation to allow for groups of different sizes, to be adopted for the Harvard housing lottery system. Our modified version of TTC will be compared against other versions of TTC, and will be optimized for strategy-proofness and runtime considerations. 

To understand the code, we generate test cases uniformly at random for houses and for allocations on preference ordering per person. We then pipe those inputs into the mechanisms we've built. alg1.py represents the Random Rankings Over Blocking Groups model. alg2.py represents the Weighted Directed Graph on Houses mechanism. Finally, alg3RSD_based.py is an instance of the RSD-based mechanism. We have commented the code within each file to allow you to better understand how our models process information and countings of matchings. 
