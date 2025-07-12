# pytoolkit-option

型安全性と関数型プログラミング機能を備えた、Rust風のOption型のPython実装

## 概要

このライブラリは、オプショナルな値を表現する`Option[T]`型を提供します。値を含む`Some[T]`か、値の不在を表す`Nothing`のいずれかを表現します。オプショナルな値にNoneを使用することを避け、null処理をより明示的で型安全にすることを目的としています。

## 機能

- **型安全なnull処理**: 値の存在・不在を明示的に処理
- **関数型プログラミングサポート**: map、and_then、match操作による計算のチェーン
- **抽象基底クラス**: Optionの直接インスタンス化を防止
- **Rust風API**: Rust開発者にとって馴染みのあるインターフェース
- **不変設計**: 安全性のためfrozenデータクラスを使用

## 必要環境

- Python 3.13+
- uv（依存関係管理用）

## インストール

```bash
uv sync
```

## 使用方法

### 基本的な使用方法

```python
from pytoolkit_option.option import Some, Nothing, Option

# 値を持つオプションを作成
some_value: Option[int] = Some(42)
print(some_value.is_some())        # True
print(some_value.unwrap())         # 42
print(some_value.unwrap_or(0))     # 42

# 空のオプションを作成
nothing: Option[int] = Nothing()
print(nothing.is_some())           # False
print(nothing.unwrap_or(0))        # 0
# nothing.unwrap()                 # ValueError が発生
```

### 関数型操作

```python
# map操作 - Someの場合に値を変換
option = Some(10).map(lambda x: x * 2)
print(option.unwrap())  # 20

# NothingでのmapはNothingを返す
nothing_result = Nothing[int]().map(lambda x: x * 2)
print(nothing_result.is_none())  # True

# and_thenで操作をチェーン
def divide_by_two(x: int) -> Option[float]:
    return Some(x / 2.0)

def to_string(x: float) -> Option[str]:
    return Some(str(x))

result = Some(10).and_then(divide_by_two).and_then(to_string)
print(result.unwrap())  # "5.0"
```

### match()によるパターンマッチング

```python
def process_option(opt: Option[int]) -> str:
    return opt.match(
        some=lambda x: f"値を取得: {x}",
        nothing=lambda: "値なし"
    )

print(process_option(Some(42)))     # "値を取得: 42"
print(process_option(Nothing()))    # "値なし"
```

### 安全な操作

```python
def safe_get_first(items: list[str]) -> Option[str]:
    if items:
        return Some(items[0])
    return Nothing[str]()

# 結果を処理
result = safe_get_first(["hello", "world"])
if result.is_some():
    print(f"最初の要素: {result.unwrap()}")
else:
    print("リストが空です")

# または、デフォルト値にunwrap_orを使用
first_item = safe_get_first([]).unwrap_or("デフォルト")
print(first_item)  # "デフォルト"
```

### メソッドチェーン

```python
# 複数の操作をチェーン
result = (Some("hello")
    .map(str.upper)                # "HELLO"
    .map(lambda s: s + " WORLD")   # "HELLO WORLD"
    .map(len))                     # 11

print(result.unwrap())  # 11
```

## APIリファレンス

### Option[T]（抽象基底クラス）

- `is_some() -> bool`: 値を含む場合にTrueを返す
- `is_none() -> bool`: 値を含まない場合にTrueを返す
- `unwrap() -> T`: 値を返すか、ValueErrorを発生させる
- `unwrap_or(default: T) -> T`: 値またはデフォルト値を返す
- `map(f: Callable[[T], U]) -> Option[U]`: Someの場合に値を変換
- `and_then(f: Callable[[T], Option[U]]) -> Option[U]`: Option返却操作をチェーン
- `match(some: Callable[[T], U], nothing: Callable[[], U]) -> U`: パターンマッチング

### Some[T]

型Tの値を含むOptionを表現します。

### Nothing[T]

値を含まないOptionを表現します。

## 開発

開発用の依存関係をインストール：

```bash
uv sync --group dev
```

テストの実行：

```bash
uv run pytest
```

型チェックの実行：

```bash
uv run pyright
```

リンティングの実行：

```bash
uv run ruff check
```

リンティング問題の修正：

```bash
uv run ruff check --fix
```

コードのフォーマット：

```bash
uv run ruff format
```

## ビルド

```bash
uv build
```

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。