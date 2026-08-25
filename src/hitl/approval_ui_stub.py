def render(queue):
    pending = queue.pending()
    return {
        "pending_count": len(pending),
        "status": "review required" if pending else "clear",
    }
