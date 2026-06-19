from enum import Enum

class HF2HelpElement(Enum):
    MaterializerStid = 0
    UVUnitSizes = 1
    CustomColors = 2
    SupportMosaic = 3
    SupportPattern = 4
    IsGrimy = 5
    Avaliability = 6
    PreviewScene = 7
    RenderIcon = 8
    InvertAlpha = 9
    MaterializerCategory = 10
    ExportMaterializer = 11
    AddMtz = 12
    DeleteMtz = 13
    AllowedRotations = 14
    PatternUsage = 15
    AddUvsizes = 16
    RemoveUvsizes = 17
    MaterializerType = 18
    MaterializerName = 19
    ModPath = 20
    MAOSTextureType = 21
    UseSmoothnessInsteadOfRoughness = 22
    NormalMapFormat = 23
    ArticlePrice = 24
    ArticleItemKind = 25
    ArticleItemSeries = 26
    ArticleAffordability = 27
    ArticleShopCategory = 28



_MaterializerCategory = "Choose category for surfacer"

_MaterializerStid = "Choose surfacer group"

_UVUnitSizes = "Set UV sizes of surfacer"

_CustomColors = "Set how many custom colors surfacer has (0-4)"

_SupportMosaic = "It is possible to use cut pattern with this materializer"

_SupportPattern = "It is possible to assign patterns to this materializer"

_IsGrimy = "If surfacer is damaged, it will decrease value of house"

_Avaliability = "Select the game modes in which surfacer will be available"

_PreviewScene = "Create preview collection for surfacer"

_RenderIcon = "Render thumbnail for surfacer"

_InvertAlpha = "If enabled, alpha channel will be set to 0 for mask map texture"

_ExportMaterializer = "Export surfacer to directory"

_AddMtz = "Create new surfacer"

_DeleteMtz = "Delete current surfacer"

_AllowedRotations = "Choose rotation for surfacer"

_PatternUsage =  "Choose surfaces for the pattern"

_AddUvsizes = "Create new UV size"

_RemoveUvsizes = "Remove selected UV size"

_MaterializerType = "Type of surfacer"

_MaterializerName = "Name of surfacer"

_ModPath = "Path to mod folder"

_InstallPillow = "Install pillow package for icon rendering"

_NormalMapFormat = "Choose used Normal Map Format (OpenGL or DirectX)"

_MAOSTextureType = "Choose whether MAOS texture is combined or splitted into seperated textures"

_UseSmoothnessInsteadOfRoughness = "Enable this if the Smoothness texture is used instead of Roughness"

_ArticlePrice = "Set price of the item in the shop"

_ArticleItemKind = "Set item kind for the item in the shop (e.g. \"Helmet\", \"Body\", \"Legs\" etc.)"

_ArticleItemSeries = "Set item series for the item in the shop"

_ArticleAffordability = "Set affordability of the item in the shop"

_ArticleShopCategory = "Set shop category for the item in the shop"


_ = [_MaterializerStid,
    _UVUnitSizes,
    _CustomColors,
    _SupportMosaic,
    _SupportPattern,
    _IsGrimy,
    _Avaliability,
    _PreviewScene,
    _RenderIcon,
    _InvertAlpha,
    _MaterializerCategory,
    _ExportMaterializer,
    _AddMtz,
    _DeleteMtz,
    _AllowedRotations,
    _PatternUsage,
    _AddUvsizes,
    _RemoveUvsizes,
    _MaterializerType,
    _MaterializerName,
    _ModPath,
    _InstallPillow,
    _MAOSTextureType,
    _UseSmoothnessInsteadOfRoughness,
    _NormalMapFormat,
    _ArticlePrice,
    _ArticleItemKind,
    _ArticleItemSeries,
    _ArticleAffordability,
    _ArticleShopCategory
]


def help_element(hf2_help_element):
    return _[hf2_help_element]




