import time
import statistics
from typing import Callable, Any, List, Dict


def measure_time(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Executa uma função uma vez e mede o tempo de execução.

    Retorna:
    - result: resultado devolvido pela função
    - elapsed_us: tempo em microsegundos
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    elapsed_us = (end - start) * 1_000_000
    return result, elapsed_us


def benchmark_operation(
    func: Callable,
    *args,
    repeats: int = 30,
    warmup: int = 3,
    **kwargs
) -> List[float]:
    """
    Mede o tempo de execução de uma operação várias vezes.

    Parâmetros:
    - func: função a medir
    - *args, **kwargs: argumentos da função
    - repeats: número de medições guardadas
    - warmup: execuções iniciais ignoradas, para estabilizar o ambiente

    Retorna:
    - lista com os tempos em microsegundos
    """
    if repeats <= 0:
        raise ValueError("repeats deve ser maior que 0")

    if warmup < 0:
        raise ValueError("warmup não pode ser negativo")

    # Warm-up
    for _ in range(warmup):
        func(*args, **kwargs)

    times_us = []

    for _ in range(repeats):
        _, elapsed_us = measure_time(func, *args, **kwargs)
        times_us.append(elapsed_us)

    return times_us


def compute_stats(times_us: List[float]) -> Dict[str, float]:
    """
    Calcula estatísticas básicas a partir de uma lista de tempos.

    Retorna um dicionário com:
    - mean_us
    - stdev_us
    - min_us
    - max_us
    - median_us
    - runs
    """
    if not times_us:
        raise ValueError("A lista de tempos não pode estar vazia")

    stats = {
        "runs": len(times_us),
        "mean_us": statistics.mean(times_us),
        "stdev_us": statistics.stdev(times_us) if len(times_us) > 1 else 0.0,
        "min_us": min(times_us),
        "max_us": max(times_us),
        "median_us": statistics.median(times_us),
    }

    return stats


def print_stats(label: str, stats: Dict[str, float]) -> None:
    """
    Imprime estatísticas de forma legível.
    """
    print(f"\n--- {label} ---")
    print(f"Runs      : {stats['runs']}")
    print(f"Média     : {stats['mean_us']:.3f} µs")
    print(f"Desvio    : {stats['stdev_us']:.3f} µs")
    print(f"Mínimo    : {stats['min_us']:.3f} µs")
    print(f"Máximo    : {stats['max_us']:.3f} µs")
    print(f"Mediana   : {stats['median_us']:.3f} µs")


def benchmark_and_summarize(
    func: Callable,
    *args,
    repeats: int = 30,
    warmup: int = 3,
    **kwargs
) -> Dict[str, Any]:
    """
    Função auxiliar que:
    1. executa o benchmark
    2. calcula estatísticas
    3. devolve tudo junto

    Retorna:
    {
        "times_us": [...],
        "stats": {...}
    }
    """
    times_us = benchmark_operation(
        func,
        *args,
        repeats=repeats,
        warmup=warmup,
        **kwargs
    )

    stats = compute_stats(times_us)

    return {
        "times_us": times_us,
        "stats": stats
    }


if __name__ == "__main__":
    # Exemplo simples de teste

    def example_function(n: int) -> int:
        total = 0
        for i in range(n):
            total += i
        return total

    result = benchmark_and_summarize(example_function, 10000, repeats=20, warmup=2)
    print_stats("Teste example_function", result["stats"])