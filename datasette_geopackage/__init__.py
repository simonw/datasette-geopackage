from datasette import hookimpl


@hookimpl
def startup(datasette):
    async def init():
        db = datasette.add_memory_database("gis")
        await db.execute_write("select InitSpatialMetadata(1)")
        print(db)

    return init


@hookimpl
def prepare_connection(conn, database):
    if database == "gis":
        return
    # Connect in the GIS database
    conn.execute("attach database 'file:gis?mode=memory&cache=shared' as gis")
    try:
        # Create a temporary view exposing SRIDs to database
        conn.execute(
            "create temporary view spatial_ref_sys as select * from gis.spatial_ref_sys"
        )
    except:
        # Was probably a read-only connection
        pass
