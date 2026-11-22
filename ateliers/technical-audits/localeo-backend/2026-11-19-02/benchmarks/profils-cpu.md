# Profils CPU

Temps CPU processus en ms dans les bruts, quantification Windows à rappeler. M01 dominé par attente injectée ; M02 simulation sans profil contention. Profils suivants distincts des timings ; aucune correction comparée.

## CSV 10 000

```text
Thu Nov 19 16:17:42 2026    D:\OneDrive\Bureau\Documents\GitHub\localeo-backend\tmp\performance-audit-2026-11-19-02\csv-10000.pstats

         460006 function calls in 0.370 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.177    0.177    0.370    0.370 export_financier.py:13(produire_csv)
    10001    0.050    0.000    0.050    0.000 {method 'writerow' of '_csv.writer' objects}
   110000    0.031    0.000    0.031    0.000 {method 'startswith' of 'str' objects}
   110000    0.029    0.000    0.029    0.000 {method 'append' of 'list' objects}
   110000    0.028    0.000    0.028    0.000 {method 'get' of 'dict' objects}
    10001    0.027    0.000    0.027    0.000 test_csv.py:262(rows)
   110000    0.027    0.000    0.027    0.000 {method 'lstrip' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'getvalue' of '_io.StringIO' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _csv.writer}
```

## Population 10 000

```text
Thu Nov 19 16:17:53 2026    D:\OneDrive\Bureau\Documents\GitHub\localeo-backend\tmp\performance-audit-2026-11-19-02\population-10000.pstats

         88855 function calls in 0.074 seconds

   Ordered by: cumulative time
   List reduced from 27 to 12 due to restriction <12>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.073    0.073 test_population.py:19(exercise)
        1    0.000    0.000    0.053    0.053 {built-in method builtins.all}
        7    0.018    0.003    0.052    0.007 test_population.py:22(<genexpr>)
    34388    0.024    0.000    0.034    0.000 uuid.py:291(__eq__)
        1    0.000    0.000    0.020    0.020 <string>:2(__init__)
        1    0.008    0.008    0.020    0.020 tirage_animation.py:76(__post_init__)
    10006    0.008    0.000    0.012    0.000 uuid.py:319(__hash__)
    34391    0.010    0.000    0.010    0.000 {built-in method builtins.isinstance}
    10006    0.004    0.000    0.004    0.000 {built-in method builtins.hash}
        1    0.000    0.000    0.000    0.000 tirage_animation.py:82(selectionner)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 random.py:365(sample)
```

Contrôles du harness inclus : pas un CPU/requête API, pas de saturation ou tendance historique démontrée.
