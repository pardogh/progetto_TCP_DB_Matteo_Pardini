-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 19, 2023 alle 22:55
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `azienda`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `dipendenti`
--

CREATE TABLE `dipendenti` (
  `id_dipendente` int(11) NOT NULL,
  `nome` varchar(30) NOT NULL,
  `cognome` varchar(30) NOT NULL,
  `posizione_lavorativa` varchar(100) NOT NULL,
  `data_assunzione` date NOT NULL,
  `email` varchar(50) NOT NULL,
  `residenza` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `dipendenti`
--

INSERT INTO `dipendenti` (`id_dipendente`, `nome`, `cognome`, `posizione_lavorativa`, `data_assunzione`, `email`, `residenza`) VALUES
(1, 'Marco', 'Rossi', 'Sviluppatore software', '2022-01-15', 'marco.rossi@email.com', 'Milano, Italia'),
(2, 'Laura', 'Bianchi', 'Responsabile delle risorse umane', '2021-03-10', 'laura.bianchi@email.com', 'Roma, Italia'),
(3, 'Giovanni', 'Verdi', 'Amministratore di sistema', '2020-07-22', 'giovanni.verdi@email.com', 'Napoli, Italia'),
(4, 'Anna', 'Neri', 'Analista finanziario', '2023-05-05', 'anna.neri@email.com', 'Firenze, Italia'),
(5, 'Paolo', 'Gialli', 'Sviluppatore software', '2021-12-03', 'paolo.gialli@email.com', 'Torino, Italia'),
(6, 'Francesca', 'Verdi', 'Responsabile delle risorse umane', '2020-09-30', 'francesca.verdi@email.com', 'Bologna, Italia'),
(7, 'Luca', 'Marroni', 'Analista finanziario', '2022-08-17', 'luca.marroni@email.com', 'Venezia, Italia'),
(8, 'Elena', 'Russo', 'Amministratore di sistema', '2023-02-28', 'elena.russo@email.com', 'Palermo, Italia'),
(9, 'Simone', 'Gialli', 'Sviluppatore software', '2021-07-14', 'simone.gialli@email.com', 'Genova, Italia'),
(10, 'Alessia', 'Bianchi', 'Analista finanziario', '2020-11-26', 'alessia.bianchi@email.com', 'Bari, Italia'),
(11, 'Paolo', 'Bianchi', 'Manager', '2023-09-22', 'paolo.bianchi@example.com', 'Genova'),
(12, 'Alessia', 'Russo', 'Contabile', '2023-06-25', 'alessia.russo@example.com', 'Bologna'),
(28, 'Francesco', 'Battaglia', 'Analista', '2022-07-13', 'france.batta@email.com', 'Reggiolo, Italia'),
(29, 'Matteo', 'Pardini', 'Informatico', '2022-10-11', 'pardo@email.com', 'Fabbrico'),
(30, 'Lorenzo', 'Galli', 'Ingegnere della pussy', '2023-10-30', 'galli.lorenzo@babilonclub.rol', 'Rolo, Italia'),
(37, 'Francesco', 'Totti', 'Re di Roma', '2020-11-20', 'francototti@mail.com', 'A gittà eterna, Idalia');

-- --------------------------------------------------------

--
-- Struttura della tabella `zone_di_lavoro`
--

CREATE TABLE `zone_di_lavoro` (
  `id_zona` int(11) NOT NULL,
  `nome_zona` varchar(100) NOT NULL,
  `numero_clienti` int(11) NOT NULL,
  `codice_dipendente` int(11) DEFAULT NULL,
  `dimensione` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `zone_di_lavoro`
--

INSERT INTO `zone_di_lavoro` (`id_zona`, `nome_zona`, `numero_clienti`, `codice_dipendente`, `dimensione`) VALUES
(1, 'Uffici Contabili', 25, 12, 250.5),
(2, 'Ufficio Amministrazione', 15, 3, 300.2),
(3, 'Uffici Informatici', 30, 1, 200.7),
(4, 'Ufficio Manager', 10, 11, 150.3),
(5, 'Ufficio Risorse Umane', 8, 2, 180.8),
(6, 'Ufficio Analisi', 5, 4, 500.1);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `dipendenti`
--
ALTER TABLE `dipendenti`
  ADD PRIMARY KEY (`id_dipendente`);

--
-- Indici per le tabelle `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD PRIMARY KEY (`id_zona`),
  ADD KEY `cod_d` (`codice_dipendente`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `dipendenti`
--
ALTER TABLE `dipendenti`
  MODIFY `id_dipendente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD CONSTRAINT `zone_di_lavoro_ibfk_1` FOREIGN KEY (`codice_dipendente`) REFERENCES `dipendenti` (`id_dipendente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
