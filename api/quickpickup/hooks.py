# Singleton registry, not great, but it works
REGISTRY = {}


def handle(obj_type, operation, _id=None, obj=None):
    """
    Handle object hook.

    Args:
        obj_type: Object type name
        operation: Operation name
        _id: Unique ID if avaialble
        obj: Object handled

    """
    handler = REGISTRY.get(obj_type, None)
    if not handler:
        return

    handler = getattr(handler, operation, None)
    if not handler:
        return

    return handler(_id, obj)


def register(obj_type, handler):
    """
    Registers a handler for *obj_type*.

    A handler class must have named methods that match operations such as
    "create", "read", "update" and "delete".

    Args:
        obj_type: Object type name
        handler: Handler class

    """
    REGISTRY[obj_type] = handler
