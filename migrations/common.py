def get_query_check_column(table: str, column: str, schema: str = "public"):
    return f"""
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema='{schema}' 
        AND table_name='{table}' 
        AND column_name='{column}'
    );"""
