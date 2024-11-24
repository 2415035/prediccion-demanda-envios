import supabase

# Configurar la conexión a Supabase
SUPABASE_URL = 'https://sjlphygbvmlrvcidfkoc.supabase.co'  # Cambia esto por tu URL de Supabase
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqbHBoeWdidm1scnZjaWRma29jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIzMzI0MTAsImV4cCI6MjA0NzkwODQxMH0.GC6jZ8OcDlza6t2W9uHjpALJ9kMLjUNGfSaT97OUL84'  # Obtén tu clave API desde tu proyecto en Supabase

# Crear cliente de conexión
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)