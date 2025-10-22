SELECT
    a.nombre_comercial,
    pr.resultado,
    COUNT(pr.id_prueba) AS total_pruebas
FROM
    PruebaResistencia pr
JOIN Antibiotico a ON pr.id_antibiotico = a.id_antibiotico
GROUP BY
    a.nombre_comercial, pr.resultado
ORDER BY
    a.nombre_comercial, pr.resultado DESC;

********

SELECT
    i.nombre || ' ' || i.apellido AS investigador_completo,
    COUNT(DISTINCT c.id_microorganismo) AS total_especies_aisladas
FROM
    Investigador i
JOIN Muestra mstr ON i.dni_investigador = mstr.dni_investigador
JOIN Placa p ON mstr.id_muestra = p.id_muestra
JOIN Colonia c ON p.codigo_placa = c.codigo_placa
GROUP BY
    i.nombre, i.apellido, i.dni_investigador
ORDER BY
    total_especies_aisladas DESC;

********

SELECT
    m.genero || ' ' || m.especie AS especie_completa,
    COUNT(pr.id_antibiotico) AS total_antibioticos_resistentes
FROM
    PruebaResistencia pr
JOIN CultivoSuspendido cs ON pr.id_cultivo_suspendido = cs.id_CultivoSuspendido
JOIN Repique r ON cs.id_repique = r.id_repique
JOIN Colonia c ON r.id_colonia = c.id_colonia AND r.codigo_placa = c.codigo_placa
JOIN Microorganismo m ON c.id_microorganismo = m.id_microorganismo
WHERE
    pr.resultado = 'resistente'
GROUP BY
    m.genero, m.especie
HAVING
    COUNT(pr.id_antibiotico) > 1
ORDER BY
    total_antibioticos_resistentes DESC;