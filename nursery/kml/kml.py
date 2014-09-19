def asKml(input_geom, altitudeMode=None, uid=''):
    """
    Performs three critical functions for creating suitable KML geometries:
     - simplifies the geoms (lines, polygons only)
     - forces left-hand rule orientation
     - sets the altitudeMode shape 
       (usually one of: absolute, clampToGround, relativeToGround)
    """
    if altitudeMode is None:
        try:
            altitudeMode = settings.KML_ALTITUDEMODE_DEFAULT
        except:
            altitudeMode = None

    key = "asKml_%s_%s_%s" % (input_geom.wkt.__hash__(), altitudeMode, uid)
    kmlcache, created = KmlCache.objects.get_or_create(key=key)
    kml = kmlcache.kml_text
    if not created and kml:
        return kml

    log.debug("%s ...no kml cache found...seeding" % key)

    latlon_geom = input_geom.transform(4326, clone=True)

    if latlon_geom.geom_type in ['Polygon','LineString']:
        geom = latlon_geom.simplify(settings.KML_SIMPLIFY_TOLERANCE_DEGREES)
        # Gaurd against invalid geometries due to bad simplification
        # Keep reducing the tolerance til we get a good one
        if geom.empty or not geom.valid: 
            toler = settings.KML_SIMPLIFY_TOLERANCE_DEGREES
            maxruns = 20
            for i in range(maxruns):
                toler = toler / 3.0
                geom = latlon_geom.simplify(toler)
                log.debug("%s ... Simplification failed ... tolerance=%s" % (key,toler))
                if not geom.empty and geom.valid: 
                    break
            if i == maxruns - 1:
                geom = latlon_geom
    else:
        geom = latlon_geom

    if geom.geom_type == 'Polygon':
        geom = forceLHR(geom)

    kml = geom.kml

    if altitudeMode and geom.geom_type == 'Polygon':
        kml = kml.replace('<Polygon>', '<Polygon><altitudeMode>%s</altitudeMode><extrude>1</extrude>' % altitudeMode)
        # The GEOSGeometry.kml() method always adds a z dim = 0
        kml = kml.replace(',0 ', ',%s ' % settings.KML_EXTRUDE_HEIGHT)

    kmlcache.kml_text = kml
    kmlcache.save()
    return kml
