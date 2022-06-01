--CREATES DATABASE SCHEMA
CREATE SCHEMA IF NOT EXISTS intuitive_care;


-- BEGIN RELATORIO_CADOP TABLE --

/*Cria a tabela para salvar os dados do csv relatorio_cadop,
os atributos são baseados nos headers do arquivo*/
CREATE TABLE intuitive_care.relacao_operadoras(
	id SERIAL,
	registro_ans VARCHAR(50),
	cnpj VARCHAR(50),
	razao_social VARCHAR(255),
	nome_fantasia VARCHAR(255),
	modalidade VARCHAR(50),
	logradouro VARCHAR(50),
	numero VARCHAR(50),
	complemento VARCHAR(255),
	bairro VARCHAR(255),
	cidade VARCHAR(50),
	uf VARCHAR(2),
	cep VARCHAR(50),
	ddd VARCHAR(10),
	telefone varchar(25),
	fax VARCHAR(25),
	endereco_eletronico VARCHAR(255),
	representante VARCHAR(255),
	cargo_representante VARCHAR(255),
	data_registro_ans DATE,
	PRIMARY KEY (id)
);

/*Popula a tabela relacao_operadoras utilizando o arquivo
relatorio_cadop.csv localizado no diretório local
(necessário mudar para o caminho local para rodar o comando)*/
copy intuitive_care.relacao_operadoras(registro_ans, cnpj, razao_social,
						nome_fantasia, modalidade, logradouro, numero, complemento,
						bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico,
						representante, cargo_representante, data_registro_ans)
FROM 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

/*Mostra a tabela depois de populada*/
SELECT * FROM intuitive_care.relacao_operadoras;
-- END RELATORIO_CADOP TABLE --



-- BEGIN DESMOSNTRACOES_CONTABEIS (2020 - 2021) TABLE --
CREATE TABLE intuitive_care.demonstracoes_contabeis(
	id SERIAL,
	data_registro DATE,
	reg_ans VARCHAR(50),
	cd_conta_contabil VARCHAR(50),
	descricao VARCHAR(255),
	vl_saldo_inicial VARCHAR(50),
	vl_saldo_final VARCHAR(50),
	PRIMARY KEY (id)
);

/*Função para iterar sobre todos os arquivos csv que populam a tabela demonstracoes_contabeis*/
DO $$
DECLARE
	files text[]:=ARRAY[
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2020\1T2020.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2020\2T2020.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2020\3T2020.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2020\4T2020.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2021\1T2021.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2021\2T2021.csv',
			 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2021\3T2021.csv'];
	copy_command text;
	csv_file text;
BEGIN
	FOREACH csv_file IN ARRAY files
		LOOP
			copy_command:='COPY intuitive_care.demonstracoes_contabeis(data_registro, reg_ans,
											cd_conta_contabil, descricao, vl_saldo_final)
			FROM '''||csv_file || '''
			DELIMITER '';''
			CSV HEADER
			ENCODING ''WIN1252'';';
			EXECUTE copy_command;
		END LOOP;
END;
$$;

/*Comando para inserir os dados do arquivo 4T2021.csv, seprado da função de loop
por obter campos a mais (vl_saldo_inicial)*/
COPY intuitive_care.demonstracoes_contabeis(data_registro, reg_ans,
											cd_conta_contabil, descricao,
											vl_saldo_inicial, vl_saldo_final)
FROM 'D:\Documentos\2-Pessoal\IntuitiveCare\Testes_01_02\static\2021\4T2021.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

/*Comando para atualizar tabelas trocando a vígula como separados dos números financeiros
da coluna vl_saldo_inicial e vl_saldo_final*/
UPDATE intuitive_care.demonstracoes_contabeis
SET vl_saldo_inicial = REPLACE(vl_saldo_inicial, ',', '.')
WHERE vl_saldo_inicial is not null;

UPDATE intuitive_care.demonstracoes_contabeis
SET vl_saldo_final = REPLACE(vl_saldo_final, ',', '.');

/*Troca o tipo de dado das colunas vl_saldo_inicial e saldo_final
de VARCHAR para double precision para possibilitar oeprações núemricas*/
ALTER TABLE intuitive_care.demonstracoes_contabeis
ALTER COLUMN vl_saldo_inicial TYPE DOUBLE PRECISION
USING CAST(vl_saldo_inicial AS DOUBLE PRECISION);

ALTER TABLE intuitive_care.demonstracoes_contabeis
ALTER COLUMN vl_saldo_final TYPE DOUBLE PRECISION
USING CAST(vl_saldo_final AS DOUBLE PRECISION);
-- END DESMOSNTRACOES_CONTABEIS (2020 - 2021) TABLE --

-- BEGIN Queries analíticas--

/*  Quais as 10 operadoras que mais tiveram despesas com
	"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS
	DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre? */

/* Agrupa os dados pelo reg_ans e soma todos os
vl_saldo_finais referentes a ele no perído do último trimestre*/
CREATE TEMP TABLE calculo_gastos AS
	SELECT 	reg_ans, ROUND(CAST(SUM(vl_saldo_final) AS NUMERIC), 2) AS gasto
	FROM intuitive_care.demonstracoes_contabeis
	WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
		AND data_registro = '2021-10-01'
	GROUP BY reg_ans
	ORDER BY gasto DESC
	LIMIT 10;

/*Left outter join para recuperar os nomes fantasias
dos reg_ans que também estão registrados na tabela
relacao_operadoras*/
SELECT cg.reg_ans, ro.nome_fantasia, cg.gasto
FROM calculo_gastos AS cg
LEFT OUTER JOIN intuitive_care.relacao_operadoras AS ro ON cg.reg_ans = ro.registro_ans;


/*	Quais as 10 operadoras que mais tiveram despesas com
	"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS
	DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano?*/

/* Agrupa os dados pelo reg_ans e soma todos os
vl_saldo_finais referentes a ele no perído do último ano*/
CREATE TEMP TABLE calculo_gastos_ultimo_ano AS
	SELECT reg_ans, ROUND(CAST(SUM(vl_saldo_final) AS NUMERIC), 2) AS gasto
	FROM intuitive_care.demonstracoes_contabeis
	WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
		AND EXTRACT('year' from data_registro) = 2021
	GROUP BY reg_ans
	ORDER BY gasto DESC
	LIMIT 10;

/*Left outter join para recuperar os nomes fantasias
dos reg_ans que também estão registrados na tabela
relacao_operadoras*/
SELECT cg.reg_ans, ro.nome_fantasia, cg.gasto
FROM calculo_gastos_ultimo_ano AS cg
LEFT OUTER JOIN intuitive_care.relacao_operadoras AS ro ON cg.reg_ans = ro.registro_ans;
-- END Queries analíticas--