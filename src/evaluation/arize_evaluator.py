def evaluate(decisions):
    return {'count': len(decisions), 'average_confidence': sum(d.confidence for d in decisions) / max(len(decisions), 1)}
