"""Módulo para transformação de vazão em Energia Natural Afluente."""

import pandas as pd

from pandas.errors import ParserError

from ena_ons import regras


class VazaoENA:
    """Classe para transformação vazão -> ENA."""

    def __init__(
        self,
        dados: pd.DataFrame,
        produtibilidade: pd.DataFrame,
    ) -> None:
        """
        Inicialização da classe.

        Parameters
        ----------
        dados : pd.DataFrame
            Dataframe com postos como colunas, datas como index e valores sendo vazão.
        produtibilidade : pd.DataFrame:
            Dataframe com colunas "codigo", "produtibilidade" para todos os postos com
            valor de produtibilidade.
        agrupamentos : pd.DataFrame
            Agrupamentos desejados para agrupar valores de ENA.
        """
        self.dados = self.__validar_dados__(dados)
        self.produtibilidade = self.__validar_produtibilidade__(produtibilidade)

    def __validar_dados__(self, dados: pd.DataFrame) -> pd.DataFrame:
        """
        Valida dataframe "dados" passado na inicialização da classe.

        Parameters
        ----------
        dados : pd.DataFrame
            Dataframe com postos como colunas, datas como index e valores sendo vazão.

        Returns
        -------
        pd.DataFrame
            Dados validados.

        Raises
        ------
        ValueError
            Caso dado passado na construção da classe não possa ser validado por algum
            motivo.
        """
        if dados.columns.dtype not in [int, float]:
            try:
                dados.columns = dados.columns.astype(float)
            except ValueError:
                raise ValueError(
                    "Colunas do dataframe de dados devem ser códigos dos postos, "
                    "no tipo int ou float!"
                )

        if not pd.api.types.is_datetime64_dtype(dados.index):
            try:
                dados.index = pd.to_datetime(dados.index)
            except (ValueError, ParserError):
                raise ValueError(
                    "Index do dataframe deve ser do tipo datetime64 ou parseável!"
                )

        return dados

    def __validar_produtibilidade__(
        self, produtibilidade: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Valida dataframe "produtibilidade" passado na inicialização da classe.

        Parameters
        ----------
        produtibilidade : pd.DataFrame
            Dataframe com colunas "codigo", "produtibilidade" para todos os postos com
            valor de produtibilidade.

        Returns
        -------
        pd.DataFrame
            Dataframe validado.

        Raises
        ------
        ValueError
            Caso dado passado na construção da classe não possa ser validado por algum
            motivo.
        """
        colunas_necessarias = ["codigo", "produtibilidade"]
        for coluna in colunas_necessarias:
            if coluna not in produtibilidade.columns:
                raise ValueError(
                    f"Dataframe de produtibilidade deve conter coluna '{coluna}'!"
                )

        produtibilidade["codigo"] = produtibilidade.codigo.astype(float)
        produtibilidade["produtibilidade"] = produtibilidade.produtibilidade.astype(
            float
        )
        return produtibilidade

    def __validar_hidrograma__(self, hidrograma: pd.DataFrame) -> pd.DataFrame:
        """
        Valida dataframe "hidrograma_belo_monte_" passado na inicialização da classe.

        Parameters
        ----------
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.

        Returns
        -------
        pd.DataFrame
            Hidrograma validado.

        Raises
        ------
        ValueError
            Caso dataframe não possa ser validado.
        """
        colunas_necessarias = ["mes", "vazao"]
        for coluna in colunas_necessarias:
            if coluna not in hidrograma.columns:
                raise ValueError(
                    f"Dataframe do hidrograma deve conter coluna '{coluna}'!"
                )
        hidrograma["mes"] = hidrograma.mes.astype(int)
        hidrograma["vazao"] = hidrograma.vazao.astype(float)
        return hidrograma

    def __validar_agrupamento__(self, agrupamento: pd.DataFrame) -> pd.DataFrame:
        """
        Valida dataframe de agrupamento.

        Dataframe deve conter apenas coluna "codigo" + 01 coluna de agrupamento especí
        fico para cálculo de soma agrupada.

        Parameters
        ----------
        agrupamento : pd.DataFrame
            Dataframe passado na função.

        Returns
        -------
        pd.DataFrame
            Agrupamento validado.

        Raises
        ------
        ValueError
            Caso dataframe não possa ser validado.
        """
        if len(agrupamento.columns) != 2:
            raise ValueError(
                f"Há {len(agrupamento.columns)} presentes no dataframe."
                "Devem existir duas colunas!"
            )

        if "codigo" not in agrupamento.columns:
            raise ValueError("Dataframe de agrupamento deve conter coluna 'codigo'!")

        return agrupamento

    @staticmethod
    def calcular_artificiais_alto_tiete(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Alto Tietê.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Alto Tietê.
        """
        traicao = regras.Traicao(df).calcular()
        pedreira = regras.Pedreira(df).calcular()
        billings_pedras = regras.BillingsPedras(df).calcular()
        pedras = regras.Pedras(df).calcular()
        edgard_souza = regras.EdgardSouza(df).calcular()
        henry_borden = regras.HenryBorden(df).calcular()
        billings_artificial = regras.BillingsArtificial(df).calcular()
        bbonita = regras.BarraBonitaArtificial(df).calcular()
        bariri_art = regras.BaririArtificial(df).calcular()
        ibitinga_art = regras.IbitingaArtificial(df).calcular()
        promissao_art = regras.PromissaoArtificial(df).calcular()
        navanhandava_art = regras.NovaAvanhandavaArtificial(df).calcular()
        tres_irmaos_art = regras.TresIrmaosArtificial(df).calcular()
        ilha_solteira = regras.IlhaSolteiraEquivalente(df).calcular()
        jupia_art = regras.JupiaArtificial(df).calcular()
        pprimavera_art = regras.PortoPrimaveraArtificial(df).calcular()
        itaipu_art = regras.ItaipuArtificial(df).calcular()

        df_alto_tiete = pd.concat(
            [
                traicao,
                pedreira,
                billings_pedras,
                pedras,
                edgard_souza,
                henry_borden,
                billings_artificial,
                bbonita,
                bariri_art,
                ibitinga_art,
                promissao_art,
                navanhandava_art,
                tres_irmaos_art,
                ilha_solteira,
                jupia_art,
                pprimavera_art,
                itaipu_art,
            ],
            axis=1,
        )

        return df_alto_tiete

    @staticmethod
    def calcular_artificiais_paraiba_sul(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Paraíba do Sul.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Paraíba do Sul.
        """
        bombeamento_sta_cecilia = regras.BombeamentoSantaCecilia(df).calcular()
        vertimento_tocos = regras.VertimentoTocos(df).calcular()
        santana_natural = regras.SantanaNatural(df).calcular()
        santana_art = regras.SantanaArtificial(df).calcular()
        vigario_art = regras.VigarioArtificial(df).calcular()
        vertimento_santana = regras.VertimentoSantana(df).calcular()
        anta_art = regras.AntaArtificial(df).calcular()
        simplicio_art = regras.SimplicioArtificial(df).calcular()
        ilha_pombos_art = regras.IlhaPombosArtificial(df).calcular()
        nilo_pecanha_art = regras.NiloPecanhaArtificial(df).calcular()
        lajes_art = regras.LajesArtificial(df).calcular()
        fontes_art = regras.FontesArtificial(df).calcular()
        pereira_passos_art = regras.PereiraPassosArtificial(df).calcular()

        df_paraiba_sul = pd.concat(
            [
                bombeamento_sta_cecilia,
                vertimento_tocos,
                santana_natural,
                santana_art,
                vigario_art,
                vertimento_santana,
                anta_art,
                simplicio_art,
                ilha_pombos_art,
                nilo_pecanha_art,
                lajes_art,
                fontes_art,
                pereira_passos_art,
            ],
            axis=1,
        )

        return df_paraiba_sul

    @staticmethod
    def calcular_naturais_sao_francisco(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do São Francisco.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do São Francisco.
        """
        pafonso = regras.PauloAfonsoNatural(df).calcular()
        complexo = regras.ComplexoNatural(df).calcular()

        df_sf = pd.concat([pafonso, complexo], axis=1)

        return df_sf

    @staticmethod
    def calcular_artificiais_iguacu(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões artificiais da bacia do Iguaçu.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Iguaçu.
        """
        jordao = regras.JordaoArtificial(df).calcular()
        segredo = regras.SegredoArtificial(df).calcular()

        df_iguacu = pd.concat([jordao, segredo], axis=1)

        return df_iguacu

    @staticmethod
    def calcular_naturais_grande(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do Grande.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do Grande.
        """
        regra = regras.ItutingaNatural(df).calcular()
        df = regra.to_frame()
        return df

    @staticmethod
    def calcular_naturais_paraguai(df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera vazões naturais da bacia do Paraguai.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.

        Returns
        -------
        pd.DataFrame
            Vazões Naturais do Paraguai.
        """
        regra = regras.ItiquiraII(df).calcular()
        df = regra.to_frame()
        return df

    @staticmethod
    def calcular_artificiais_xingu(
        df: pd.DataFrame, hidrograma: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Gera vazões artificial da bacia do Xingu.

        Memorial de cálculo pode ser encontrado no arquivo
        "Atualização de Séries Históricas de Vazões".

        Parameters
        ----------
        df : pd.DataFrame
            Dados coletados do ACOMPH.
        hidrograma : pd.DataFrame
            Vazões do hidrograma (médio) de Belo Monte por mês.

        Returns
        -------
        pd.DataFrame
            Vazões Artificiais do Xingu.
        """
        belomonte = regras.BeloMonteArtificial(df, hidrograma).calcular()
        pimental_art = regras.PimentalArtificial(df, hidrograma).calcular()

        df_xingu = pd.concat([belomonte, pimental_art], axis=1)

        return df_xingu

    def adicionar_vazoes_artificiais(self, hidrograma: pd.DataFrame) -> pd.DataFrame:
        """
        Adiciona vazões artificiais aos dados de vazão da entrada.

        Parameters
        ----------
        hidrograma : pd.DataFrame
            Hidrograma (médio) de Belo Monte. Deve ser um dataframe contendo uma coluna
            chamada "mes", com os meses do ano e coluna "vazao" contendo os valores de
            desvio mínimo.

        Returns
        -------
        pd.DataFrame
            Dataframe com vazão natural afluente diária por posto.
        """
        hidrograma = self.__validar_hidrograma__(hidrograma)

        df = self.dados.copy()
        df_alto_tiete = self.calcular_artificiais_alto_tiete(df)
        df_paraiba_sul = self.calcular_artificiais_paraiba_sul(df)
        df_sf = self.calcular_naturais_sao_francisco(df)
        df_iguacu = self.calcular_artificiais_iguacu(df)
        df_grande = self.calcular_naturais_grande(df)
        df_paraguai = self.calcular_naturais_paraguai(df)
        df_xingu = self.calcular_artificiais_xingu(df, hidrograma)

        return pd.concat(
            [
                df,
                df_alto_tiete,
                df_paraiba_sul,
                df_sf,
                df_iguacu,
                df_grande,
                df_paraguai,
                df_xingu,
            ],
            axis=1,
        )

    def calcular_ena(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula valores de ENA por posto.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe com valores de vazão.

        Returns
        -------
        pd.DataFrame
            Dataframe com valores de ENA.
        """
        df_melt = df.melt(
            value_name="valor", var_name="codigo", ignore_index=False
        ).reset_index()
        df_prod = df_melt.merge(self.produtibilidade, on="codigo", how="left")
        df_prod = df_prod.assign(ena=df_prod.valor * df_prod.produtibilidade)

        df_ena = df_prod[["data", "codigo", "ena"]].pivot(
            index="data", columns="codigo", values="ena"
        )
        return df_ena

    def agrupar(self, df: pd.DataFrame, agrupamento: pd.DataFrame) -> pd.DataFrame:
        """
        Soma valores de ENA a partir do agrupamento passado.

        Parameters
        ----------
        df : pd.DataFrame
            Valores calculados de ENA por posto.
        agrupamento : pd.DataFrame
            Dataframe deve conter apenas coluna "codigo" + 01 coluna de agrupamento
            específico para cálculo de soma agrupada.

        Returns
        -------
        pd.DataFrame
            ENA somada por agrupamento.
        """
        agrupamento = self.__validar_agrupamento__(agrupamento)
        for coluna in agrupamento.columns:
            if coluna != "codigo":
                grupo = coluna

        df_melt = df.melt(
            value_name="valor", var_name="codigo", ignore_index=False
        ).reset_index()
        df_relacao = df_melt.merge(agrupamento, on="codigo", how="left")

        df_agrupado = df_relacao[["data", grupo, "valor"]]
        df_agrupado = df_agrupado.groupby(["data", grupo]).sum().reset_index()
        df_pivotado = df_agrupado.pivot(index="data", columns=grupo, values="valor")

        return df_pivotado
