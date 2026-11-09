from runtime.story_engine import StoryEngine


def set_line_and_scene(
    story_engine: StoryEngine, scene_number: int, line_number: int | None = None
) -> None:
    story_engine.validate_story()
    story_engine.set_scene(story_engine.story.get_scene(scene_number))
    if line_number is not None:
        story_engine.set_new_loc(line_number)
