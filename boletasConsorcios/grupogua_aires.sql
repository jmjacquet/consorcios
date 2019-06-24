-- phpMyAdmin SQL Dump
-- version 4.4.15
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 04-12-2015 a las 11:36:42
-- Versión del servidor: 5.5.46-37.5
-- Versión de PHP: 5.5.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `grupogua_aires`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cabanias`
--

CREATE TABLE IF NOT EXISTS `cabanias` (
  `id` int(11) NOT NULL,
  `nombre_complejo` varchar(100) NOT NULL,
  `propietario` varchar(100) DEFAULT NULL,
  `telefonos` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `web` varchar(40) DEFAULT NULL,
  `ubicacion` varchar(200) DEFAULT NULL,
  `descripcion` text,
  `tipo` varchar(30) DEFAULT NULL COMMENT 'CABANAS\r\nHOSPEDAJES\r\nHOTELES\r\nCAMPINGS\r\nCASAS-DEPARTAMENTOS'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `noticias`
--

CREATE TABLE IF NOT EXISTS `noticias` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `texto` longtext NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `noticias`
--

INSERT INTO `noticias` (`id`, `fecha`, `titulo`, `texto`) VALUES
(1, '2015-09-19', 'TORNEO DE TENIS PRIMAVERA 2015', 'Agradecemos a todos los participantes de una justa deportiva emotiva en la que los competidores demostraron un gran espíritu deportivo y de camaradería.\r\n\r\nLos esperamos en el próximo encuentro.'),
(2, '2015-03-09', 'Autoridades Asociacion Civil Aires del LLano Country Club', 'Ha quedado constituida la Asociacion Civil Aires del Llano Country Club que administra a partir del 03/09/2015 los espacios comunes del Country. También ese día se ha elegido la Comisión Directiva de la mencionada entidad quedando conformada por los siguientes miembros:\r\n\r\nCOMISION DIRECTIVA\r\n\r\nPRESIDENTE\r\n\r\nSr. Ricardo Chito\r\n\r\nSECRETARIO\r\n\r\nSr. Cristian Martinez\r\n\r\nTESORERO\r\n\r\nSr. Exequiel Angioni\r\n\r\nVOCAL TITULAR\r\n\r\nSr. Martín Guzmán\r\n\r\nVOCAL TITULAR\r\n\r\nSr. Germán Gueler\r\n\r\nVOCAL SUPLENTE Barrio 1\r\n\r\nSr. Adrian Ramirez\r\n\r\nVOCAL SUPLENTE Barrio 2\r\n\r\nSr. Alberto Boz\r\n\r\nVOCAL SUPLENTE Barrio 3\r\n\r\nSr. Alejandro Alesso\r\n\r\nVOCAL SUPLENTE Barrio 5\r\n\r\nSr. Pablo Trivero\r\n\r\nVOCAL SUPLENTE Barrio 6\r\n\r\nSr. Sebastian Zacarias\r\n\r\n \r\n\r\nREVISORES DE CUENTAS\r\n\r\nTITULAR\r\n\r\nC. P. N. Hernán Nardelli\r\n\r\nSUPLENTE\r\n\r\nC. P. N. Santiago Gerardo Rico\r\n\r\nTambién ha sido designado en el cargo de Coordinador General de la CD, el Sr. Adrian Ramirez.'),
(3, '2015-06-11', 'INSCRIPCION A DELEGADOS BARRIALES', 'La Comisión Directiva Transitoria Ampliada (CDTA) del emprendimiento denominado Aires del Llano Country Club, en uso de las facultades conferidas por la Fiduciaria de Fideicomiso Aires del Llanorecuerda que desde el 11/06/2015 hasta el 01/07/2015 estará abierta la inscripción para los postulantes de candidatos a delegados de Barrio de la Asociación Civil Sin Fines de Lucro que administrará los espacios comunes del country, la cual fuera aprobada en la REUNION DE PROPIETARIOS del 20/05/2015.\r\n\r\nTal como se viene informando el texto del Estatuto de la Asociación puede ser obtenido del siguiente link: https://www.dropbox.com/s/myblvdzkqxavb5n/Acta%20Constitutiva%20con%20Estatuto%20Aires%20del%20Llano%20Country%20Club.pdf?dl=0\r\n\r\nSe recuerda que, tal como lo indica el artículo 19, 40,  48 y concordantes del Estatuto, los socios (Fiduciantes y/o Propietarios) que se quieran inscribir a las duplas para ser delegados de Barrio deberán cumplimentar con los siguientes requisitos:\r\n\r\na) Ser Asociado de alguna de las categorías (Barrio 1, 2, 3, 5 o 6).\r\n\r\nb) Estar en el pleno goce de sus derechos como asociado y no tener inhibiciones personales, no estar concursado o quebrado.\r\n\r\nc) Estar al día con las cuotas sociales y con las demás obligaciones que surjan del estado de socio, no adeudar ningún tipo de obligación a la asociación, incluyendo multas, al día 10 del mes inmediato anterior de la fecha límite de la posibilidad de postulación.\r\n\r\nLa inscripción debe hacerse en forma personal o mediante persona autorizada o apoderado, en las oficinas de Goldriser Business & Finance S.R.L. ubicadas en calle San Martín 3472 de la ciudad de Santa Fe, provincia de Santa fe hasta el 01/07/2015 a los efectos de firmar el formulario de inscripción pertinente debiendo cumplir con los siguientes requisitos:'),
(4, '2015-05-20', 'REUNION DE PROPIETARIOS', 'La REUNION DE PROPIETARIOS a realizarse el día miércoles 20 de Mayo del 2015 a las 20:00 hs en el SALON de EVENTOS del Country tratará el siguiente ORDEN del DIA:\r\n\r\n1- Someter a consideración y votación la rectificación de la figura jurídica aprobada en Reunión de Propietarios del 26/11/2014 y 17/12/2014 (Asociación Civil sin Fines de Lucro inscripta como S. A.) para pasar a adoptar la figura de “Asociación Civil”, a fin de encuadrar legalmente el ente que tendrá por finalidad administrar los espacios comunes de Aires de Llano Country Club.\r\n\r\n2- Someter a votación el texto del estatuto de la Asociación Civil que administrará los espacios comunes elaborado conforme a los lineamientos generales aprobados en la Reunión de Propietarios del 17/12/2014 y lo resuelto en el punto 1 delpresente orden del día, propuesto por la CDTA conjuntamente con las Comisiones Internas en Reunión Plenaria de Comisiones conforme lo establecido en el Inc. X) del Art. 6 del Reglamento Interno del Country por mandato otorgado oportunamente en Reunión de Propietarios.\r\n\r\n3- Aprobar el cronograma para realizar los actos preparativos correspondientes a la constitución de la Asociación Civil que administrará los espacios comunes.\r\n\r\n4- Informe de la Subcomisión de Infraestructura y la CDTA sobre el nivel de avance de las tareas tendientes a terminar la obra relativa a la Planta de Tratamiento de Líquidos Cloacales.\r\n\r\nEl texto del estatuto mencionado en el punto 2 del orden del día y el dictamen jurídico sobre el mismo emitido por el estudio contratado para asesorar en su redacción, pueden obtenerse de los siguientes links:');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenanzas`
--

CREATE TABLE IF NOT EXISTS `ordenanzas` (
  `id` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `titulo` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `slider`
--

CREATE TABLE IF NOT EXISTS `slider` (
  `id` int(11) NOT NULL,
  `titulo` varchar(200) DEFAULT NULL,
  `subtitulo` varchar(200) DEFAULT NULL,
  `descripcion` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE IF NOT EXISTS `usuarios` (
  `usuario` varchar(30) NOT NULL,
  `password` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cabanias`
--
ALTER TABLE `cabanias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `noticias`
--
ALTER TABLE `noticias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ordenanzas`
--
ALTER TABLE `ordenanzas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `slider`
--
ALTER TABLE `slider`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cabanias`
--
ALTER TABLE `cabanias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `noticias`
--
ALTER TABLE `noticias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `ordenanzas`
--
ALTER TABLE `ordenanzas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `slider`
--
ALTER TABLE `slider`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
