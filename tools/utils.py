"""توابع کمکی برای کار با دیتافریم فوتبال (پانداس).

شامل:
- گزارش مقادیر گم‌شده در یک فصل
- نمایش ردیف‌هایی که یک ستون آن‌ها NaN است
- پر کردن یک ستون از روی دیکشنری با کلید تاپل
- تخصیص هم‌زمان چند مقدار به چند ستون برای ردیف‌های منطبق بر شرط
"""

from typing import Any, Iterable

import pandas as pd

__all__ = [
    "missing_report",
    "null_rows",
    "fill_from_dict",
    "assign_row",
    "null_count_per_season",
    "null_teams",
]



def _season_mask(df: pd.DataFrame, season: Any, season_col: str) -> pd.Series:
    """ماسک بولی برای انتخاب یک فصل (مقایسه امن از نظر نوع داده)."""
    return df[season_col].astype(str) == str(season)


# ۱) گزارش ستون‌های دارای NaN در یک فصل
def missing_report(
    df: pd.DataFrame,
    season: Any,
    season_col: str = "Season",
) -> pd.Series:
    """ستون‌هایی که در فصل مشخص، حداقل یک مقدار NaN دارند.

    خروجی: سری شامل تعداد مقادیر گم‌شده‌ی هر ستون (فقط ستون‌هایی با شمارش > ۰).
    """
    mask = _season_mask(df, season, season_col)
    na_counts = df.loc[mask].isna().sum()
    return na_counts[na_counts > 0]


# ۲) نمایش ردیف‌هایی که یک ستون مشخص در آن‌ها NaN است
def null_rows(
    df: pd.DataFrame,
    season: Any,
    column: str,
    show_cols: Iterable[str] | None = None,
    season_col: str = "Season",
) -> pd.DataFrame:
    """ردیف‌هایی که در یک فصل، مقدار ستون موردنظرشان NaN است.

    Parameters
    ----------
    column : نام ستونی که باید NaN بودنش بررسی شود.
    show_cols : ستون‌هایی که در خروجی نمایش داده شوند.
        (پیش‌فرض: HomeTeam, AwayTeam, Year, Month, Day)
    """
    mask = _season_mask(df, season, season_col) & df[column].isna()
    if show_cols is None:
        show_cols = ["HomeTeam", "AwayTeam", "Year", "Month", "Day"]
    return df.loc[mask, list(show_cols)]


# ۳) پر کردن یک ستون از روی دیکشنری با کلید تاپل
def fill_from_dict(
    df: pd.DataFrame,
    season: Any,
    data: dict[tuple, Any],
    key_cols: Iterable[str] = ("HomeTeam", "AwayTeam"),
    value_col: str = "Attendance",
    value_cols: Iterable[str] | None = None,
    season_col: str = "Season",
    inplace: bool = False,
) -> pd.DataFrame | None:
    """پر کردن یک یا چند ستون از روی دیکشنری با کلید تاپل، فقط برای یک فصل.

    دو حالت پشتیبانی می‌شود:
    1) مقدار هر کلید یک اسکالر باشد:
       {("Liverpool", "Brentford"): 52824}
       در این حالت مقدار در value_col ریخته می‌شود.

    2) مقدار هر کلید یک دیکشنری از ستون->مقدار باشد:
       {
           ("Aston Villa", "Everton"): {
               "WeekDay": "Fri",
               "Time": "20:00",
               "Round": 3
           }
       }
       در این حالت ستون‌ها از روی همان دیکشنری یا value_cols پر می‌شوند.
    """
    result = df if inplace else df.copy()
    season_mask = _season_mask(result, season, season_col)
    key_cols = list(key_cols)

    for idx in result.index[season_mask]:
        row = result.loc[idx]
        key = tuple(row[col] for col in key_cols)

        if key not in data or data[key] is None:
            continue

        item = data[key]

        if isinstance(item, dict):
            cols_to_fill = value_cols if value_cols is not None else item.keys()
            for col in cols_to_fill:
                if col in item:
                    result.loc[idx, col] = item[col]
        else:
            result.loc[idx, value_col] = item

    return None if inplace else result



# ۴) تخصیص هم‌زمان چند مقدار به چند ستون برای ردیف‌های منطبق بر شرط
def assign_row(
    df: pd.DataFrame,
    season: Any,
    conditions: dict[str, Any],
    columns: Iterable[str],
    values: Iterable[Any],
    season_col: str = "Season",
    inplace: bool = False,
) -> pd.DataFrame | None:
    """تخصیص چند مقدار به چند ستون برای ردیف‌هایی که شرط را دارند.

    Parameters
    ----------
    conditions : دیکشنری شرط‌های اضافه به‌جز فصل،
        مثلاً {"AwayTeam": "Brighton"}.
    columns : لیست ستون‌های مقصد.
    values : لیست مقادیر هم‌ترتیب با columns.
    """
    result = df if inplace else df.copy()
    mask = _season_mask(result, season, season_col)

    for col, val in conditions.items():
        mask &= result[col] == val

    result.loc[mask, list(columns)] = list(values)
    return None if inplace else result


# ۵) شمارش مقادیر NaN یک ستون به تفکیک فصل
def null_count_per_season(
    df: pd.DataFrame,
    column: str,
    season_col: str = "Season",
) -> pd.Series:
    """تعداد مقادیر گم‌شده‌ی یک ستون را به تفکیک فصل برمی‌گرداند.

    Parameters
    ----------
    column : ستونی که NaN بودنش بررسی می‌شود.
    season_col : نام ستون فصل.

    Returns
    -------
    pd.Series
        ایندکس = نام فصل، مقدار = تعداد NaN.
    """
    return df.loc[df[column].isna(), season_col].value_counts()


# ۶) تیم‌های یکتا که مقدار ستونی برای آن‌ها در یک فصل NaN است
def null_teams(
    df: pd.DataFrame,
    season: Any,
    column: str,
    team_col: str = "HomeTeam",
    season_col: str = "Season",
) -> list:
    """لیست مرتبِ تیم‌های یکتایی که مقدار ستون موردنظرشان در فصل مشخص NaN است.

    Parameters
    ----------
    season : شماره فصل (رشته یا عدد).
    column : ستونی که NaN بودنش بررسی می‌شود.
    team_col : ستون تیم (پیش‌فرض HomeTeam).
    """
    mask = _season_mask(df, season, season_col) & df[column].isna()
    teams = df.loc[mask, team_col].unique()
    return sorted(teams)
