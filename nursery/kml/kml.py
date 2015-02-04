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


def kml_errors(kmlstring):
    from madrona.common import feedvalidator
    from madrona.common.feedvalidator import compatibility
    events = feedvalidator.validateString(kmlstring, firstOccurrenceOnly=1)['loggedEvents']

    # Three levels of compatibility
    # "A" is most basic level
    # "AA" mimics online validator
    # "AAA" is experimental; these rules WILL change or disappear in future versions
    filterFunc = getattr(compatibility, "AA")
    events = filterFunc(events)

    # there are a few annoyances with feedvalidator; specifically it doesn't recognize
    # KML ExtendedData element
    # or our custom 'mm' namespance
    # or our custom atom link relation
    # or space-delimited Icon states
    # so we ignore all related events
    events = [x for x in events if not (
                (isinstance(x,feedvalidator.logging.UndefinedElement)
                    and x.params['element'] == u'ExtendedData') or
                (isinstance(x,feedvalidator.logging.UnregisteredAtomLinkRel)
                    and x.params['value'] == u'madrona.update_form') or
                (isinstance(x,feedvalidator.logging.UnregisteredAtomLinkRel)
                    and x.params['value'] == u'madrona.create_form') or
                (isinstance(x,feedvalidator.logging.UnknownNamespace)
                    and x.params['namespace'] == u'http://madrona.org') or
                (isinstance(x,feedvalidator.logging.UnknownNamespace)
                    and x.params['namespace'] == u'http://www.google.com/kml/ext/2.2') or
                (isinstance(x,feedvalidator.logging.InvalidItemIconState)
                    and x.params['element'] == u'state' and ' ' in x.params['value']) or
                (isinstance(x,feedvalidator.logging.UnregisteredAtomLinkRel)
                    and x.params['element'] == u'atom:link' and 'workspace' in x.params['value'])
                )]

    from madrona.common.feedvalidator.formatter.text_plain import Formatter
    output = Formatter(events)

    if output:
        errors = []
        for i in range(len(output)):
            errors.append((events[i],events[i].params,output[i],kmlstring.splitlines()[events[i].params['backupline']]))
        return errors
    else:
        return None
