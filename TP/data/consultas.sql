SELECT
    pm.tipo_zona,
    pr.resultado,
    COUNT(pr.id_prueba) AS total_pruebas
FROM
    PruebaResistencia pr
JOIN CultivoSuspendido cs ON pr.id_cultivo_suspendido = cs.id_CultivoSuspendido
JOIN Repique r ON cs.id_repique = r.id_repique
JOIN Colonia c ON r.id_colonia = c.id_colonia AND r.codigo_placa = c.codigo_placa
JOIN Microorganismo m ON c.id_microorganismo = m.id_microorganismo
JOIN Placa p ON c.codigo_placa = p.codigo_placa
JOIN Muestra mstr ON p.id_muestra = mstr.id_muestra
JOIN PuntosDeMuestreo pm ON mstr.id_PuntoMuestreo = pm.id_PuntoMuestreo
JOIN Antibiotico a ON pr.id_antibiotico = a.id_antibiotico
WHERE
    m.genero = 'Escherichia' AND m.especie = 'coli'
    AND a.nombre_comercial = 'Penicilina'
GROUP BY
    pm.tipo_zona, pr.resultado;