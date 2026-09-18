# F08 - I/O synchrones dans les entrees asynchrones

Les handlers conservent uniquement la lecture asynchrone du corps sur la boucle
evenementielle. Le traitement Stripe Connect, le login admin avec son UoW et
les traitements de documents (stockage, inspection, SQL, serialisation) sont
executes dans le pool de threads borne Starlette. Chaque UoW est ouvert et ferme
dans le meme thread. Les handlers sans lecture asynchrone sont declares `def`.
