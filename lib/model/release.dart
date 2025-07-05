class Release {
  const Release({
    required this.id,
    required this.name,
    required this.isLocal,
    required this.isAustralian,
    required this.isDemo,
    required this.hasFemale,
  });

  final int id;
  final String name;
  final bool isLocal;
  final bool isAustralian;
  final bool isDemo;
  final bool hasFemale;
}
