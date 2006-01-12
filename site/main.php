<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?php
/**
 * DokuWiki template for site http://pyradm.berlios.de
 *
 * @link   http://wiki.splitbrain.org/wiki:tpl:templates
 * @author Alexey Remizov <alexey@remizov.pp.ru>
 */
?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $conf['lang']?>"
 lang="<?php echo $conf['lang']?>" dir="<?php echo $lang['direction']?>">
<head>
  <title><?php tpl_pagetitle()?> [<?php echo hsc($conf['title'])?>]</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

  <?php tpl_metaheaders()?>

  <link rel="stylesheet" media="screen" type="text/css" href="<?php echo DOKU_TPL?>screen.css" />
  <link rel="stylesheet" media="print" type="text/css" href="<?php echo DOKU_TPL?>print.css" />
</head>

<body>
<div class="page">

	<div class="header">
	  <h1><?php tpl_link(wl(),$conf['title'],'name="top" accesskey="h" title="[ALT+H]"')?></h1>
	  <p>CLI administration tool for Cyrus IMAP server</p>
    <?php tpl_searchform() ?>
	</div>

	<div class="navigation"> 
		<ul>
			<li><a href="/">Home</a></li>
			<li><a href="https://developer.berlios.de/projects/pyradm/">BerliOS project</a></li>
			<li><a href="doku.php?id=links">Links</a></li>
      <li><form class="button" name="indexform" method="get" action="/doku.php" onsubmit="return svchk()"><input type="hidden" name="do" value="index" /><input type="hidden" name="id" value="start" /><a onclick="document.forms.indexform.submit(); return false" href="#">Site map</a></form></li>
      <!-- li><p><strong>A tiny little service announcement.</strong><br/>Put all your little tidbits of information or pictures in this small yet useful little area. </p></li -->
		</ul>
    <div class="webbuttons">
      <a href="http://developer.berlios.de"><img src="<?php echo DOKU_TPL ?>images/bslogo.png" width="88" height="31" alt="Hosted by BerliOS" title="Hosted by BerliOS"/></a>
      <a href="http://wiki.splitbrain.org/wiki:dokuwiki"><img src="<?php echo DOKU_TPL ?>images/dwlogo.png" width="88" height="31" alt="Driven by DokuWiki" title="Driven by DokuWiki"/></a>
      <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Transitional" title="Valid XHTML 1.0 Transitional" height="31" width="88" /></a>
    </div>
    <br/>&nbsp;
  </div>

  <div class="content">
    <div class="breadcrumbs"><?php tpl_breadcrumbs()?></div>
    <?php tpl_content(); ?>
    <div class="page_controls">
      <div style="float: right">
        <?php tpl_button('edit')?>
        <?php tpl_button('top')?>
      </div>
      <?php tpl_button('login')?>
      <?php tpl_button('admin')?>
    </div>
  </div>
	  
	<div class="footer">
    <div class="pageinfo"><?php tpl_pageinfo()?></div>
    <p>Copyright &copy; 2006 Alexey Remizov | Design mostly based on work <a href="http://www.oswd.org/design/preview/id/2429">&ldquo;Leaves&rdquo;</a> by <a href="http://smallpark.org">SmallPark</a></p>
  </div>
</div>
</body>
</html>
