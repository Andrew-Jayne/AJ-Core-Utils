# AJ-Core-Utils
A set of python functions, modules and classes I end up building or using in every project.


`ensure_type`: This does runtime type validation, very very useful for making sure that the value from the `list[dict[str, dict[str,list[dict[str,int]]]]]` you made is what it should be

`load_mandatory_var`: Var loader for critical vars, if your app can't start without a DB_URL set in the env, tell people, also does not allow for defaults so people don't leak API keys. Supports returning to all standard python primitives

`load_optional_var`: Var loader for the other vars, but requires you to declare a default value rather than the implicit `None` that os.getenv() would return. Also supports returning to all standard python primities

`GatewaySingleton` Shockingly useful stateful object to inject objects you need where ever you can stick an import statement. Works best for Read Only and Non-Mutating uses like `GatewaySingleton.method()` or `GatewaySingleton.value`. Loved using this for Mongo Connections since that used a global long lived object.